# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_repair = fields.Boolean(string="It's repair", default=False, copy=True)
    created_repair_ids = fields.One2many(
        string="Created repairs",
        comodel_name="repair.order",
        inverse_name="created_from_picking_id",
        copy=True,
    )
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", store=True, copy=True
    )
    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=True
    )
    untreated_origin = fields.Char(string="Untreated origin", copy=True)
    devolution_sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=True
    )

    @api.depends("created_repair_ids")
    def _compute_repairs_count(self):
        for picking in self:
            picking.repairs_count = len(picking.created_repair_ids)

    def button_validate(self):
        result = super().button_validate()
        pickings = self.filtered(lambda x: x.state == "done")
        if pickings:
            in_pickings = pickings.filtered(
                lambda x: x.picking_type_code == "incoming" and x.is_repair
            )
            if in_pickings:
                in_pickings.create_repairs_from_picking()
            repair_pickings = pickings.filtered(
                lambda x: x.picking_type_code == "incoming"
                and x.devolution_sale_order_id
                and not x.is_repair
            )
            if repair_pickings:
                repair_pickings.put_move_in_repair_from_devolution_picking()
        return result

    def create_repairs_from_picking(self):
        for picking in self.filtered(
            lambda x: x.picking_type_code == "incoming" and x.is_repair
        ):
            for line in picking.move_line_ids.filtered(
                lambda x: x.qty_done > 0 and not x.created_repair_id
            ):
                vals = line.catch_values_from_create_repair_from_picking()
                repair = self.env["repair.order"].create(vals)
                line.created_repair_id = repair.id

    def action_repairs_from_picking(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.created_repair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_assign(self):
        for picking in self:
            lots = picking.sale_order_id.mapped("repair_ids.move_id.lot_ids")
            super(StockPicking, picking.with_context(force_lots=lots)).action_assign()
        return True

    def _get_quants_to_treat(self):
        found = False
        my_quants = self.env["stock.quant"]
        if (
            self.is_repair
            and self.picking_type_id.code == "outgoing"
            and self.sale_order_id
        ):
            repairs = self.sale_order_id.repair_ids.filtered(
                lambda x: x.state in ("2binvoiced", "done")
            )
            if repairs and self.backorder_id:
                my_repairs = self.env["repair.order"]
                for line in self.move_lines.filtered(lambda x: x.state != "cancel"):
                    if line.origin:
                        for repair in repairs:
                            x = line.origin.find(repair.name)
                            if x != -1 and repair not in my_repairs:
                                my_repairs += repair
                if my_repairs:
                    repairs = my_repairs
            if repairs:
                lots = repairs.mapped("lot_id")
                cond = [
                    ("lot_id", "in", lots.ids),
                    ("location_id", "=", self.location_id.id),
                ]
                quants = self.env["stock.quant"].search(cond)
                if quants:
                    for quant in quants:
                        cond = [
                            ("picking_id", "!=", False),
                            ("picking_type_id.code", "=", "outgoing"),
                            ("lot_id", "=", quant.lot_id.id),
                            ("state", "in", ("done", "assigned")),
                        ]
                        line = self.env["stock.move.line"].search(cond)
                        if not line:
                            my_quants += quant
                            found = True
        return found, my_quants

    def _get_quants_to_treat_to_devolution(self):
        found = False
        my_quants = self.env["stock.quant"]
        lots = self.env.context.get("default_repairs_from_devolution").mapped("lot_id")
        out_picking = self.env.context.get("default_picking_from_devolution")
        cond = [
            ("lot_id", "in", lots.ids),
            ("location_id", "=", out_picking.location_id.id),
        ]
        quants = self.env["stock.quant"].search(cond)
        if quants:
            for quant in quants:
                cond = [
                    ("picking_id", "=", out_picking.id),
                    ("lot_id", "=", quant.lot_id.id),
                    ("state", "in", ("done", "assigned")),
                ]
                line = self.env["stock.move.line"].search(cond)
                if line:
                    my_quants += quant
                    found = True
        return found, my_quants

    def _put_realized_moves_in_repairs(self):
        repair_obj = self.env["repair.order"]
        for picking in self:
            origin = ""
            new_origin = ""
            for line in picking.move_lines.filtered(lambda m: m.origin):
                origin = (
                    line.origin if not origin else "{}/{}".format(origin, line.origin)
                )
            for line in picking.move_line_ids.filtered(
                lambda z: z.is_repair
                and z.sale_line_id
                and z.lot_id
                and z.state == "done"
                and z.move_id.repair_id
            ):
                cond = [
                    ("from_repair_picking_out_id", "=", picking.id),
                    ("sale_line_id", "=", line.sale_line_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("state", "in", ("done", "2binvoiced")),
                ]
                repairs = repair_obj.search(cond)
                my_repairs = self.env["repair.order"]
                if repairs and origin:
                    for repair in repairs:
                        x = origin.find(repair.name)
                        if x != -1 and repair not in my_repairs:
                            my_repairs += repair
                    repairs = my_repairs
                if repairs:
                    repairs.write({"move_id": False})
                    repairs_not_to_treat = repairs.filtered(
                        lambda x: x.lot_id != line.lot_id
                    )
                    repairs_to_treat = repairs.filtered(
                        lambda x: x.lot_id == line.lot_id
                    )
                origin = ""
                for repair in repairs_not_to_treat:
                    origin = (
                        repair.name
                        if not origin
                        else "{}/{}".format(origin, repair.name)
                    )
                for repair in repairs_to_treat:
                    new_origin = (
                        repair.name
                        if not new_origin
                        else "{}/{}".format(new_origin, repair.name)
                    )
                    if not repair.move_id:
                        repair.move_id = line.move_id.id
                line.move_id.origin = new_origin
            picking.untreated_origin = origin

        if "created_new_picking" in self.env.context:
            self._put_origin_in_treated_move_lines(origin)
            self.process_new_delivery_picking_created(origin)

    def _put_origin_in_treated_move_lines(self, origin):
        repair_obj = self.env["repair.order"]
        for picking in self:
            for line in picking.move_lines.filtered(
                lambda x: x.state == "cancel" and x.sale_line_id and x.is_repair
            ):
                cond = [
                    ("from_repair_picking_out_id", "=", picking.id),
                    ("sale_line_id", "=", line.sale_line_id.id),
                    ("product_id", "=", line.product_id.id),
                    ("state", "in", ("done", "2binvoiced")),
                    ("move_id", "=", False),
                ]
                repairs = repair_obj.search(cond)
                my_repairs = self.env["repair.order"]
                if repairs and picking.origin:
                    for repair in repairs:
                        x = origin.find(repair.name)
                        if x != -1 and repair not in my_repairs:
                            my_repairs += repair
                    repairs = my_repairs
                origin = ""
                if repairs:
                    line.origin = ""
                for repair in repairs:
                    origin = (
                        repair.name
                        if not origin
                        else "{}, {}".format(origin, repair.name)
                    )
                    if not repair.move_id:
                        repair.move_id = line.id
                if origin:
                    line.origin = origin

    def process_new_delivery_picking_created(self, origin):
        repair_obj = self.env["repair.order"]
        for picking in self:
            cond = [("backorder_id", "=", picking.id)]
            new_picking = self.env["stock.picking"].search(cond, limit=1)
            if new_picking:
                new_picking.write(
                    {"sale_order_id": picking.sale_order_id.id, "is_repair": True}
                )
                for line in new_picking.move_lines:
                    line.origin = picking.untreated_origin
                    cond = [
                        ("from_repair_picking_out_id", "=", picking.id),
                        ("sale_line_id", "=", line.sale_line_id.id),
                        ("product_id", "=", line.product_id.id),
                        ("state", "in", ("done", "2binvoiced")),
                        ("move_id", "=", False),
                    ]
                    repairs = repair_obj.search(cond)
                    if repairs:
                        my_repairs = self.env["repair.order"]
                        if repairs and picking.origin:
                            for repair in repairs:
                                x = origin.find(repair.name)
                                if x != -1 and repair not in my_repairs:
                                    my_repairs += repair
                            repairs = my_repairs
                    repairs.write(
                        {
                            "from_repair_picking_out_id": new_picking.id,
                            "move_id": line.id,
                        }
                    )
                if new_picking.state == "assigned":
                    new_picking.do_unreserve()

    def put_move_in_repair_from_devolution_picking(self):
        for picking in self:
            for move_line in picking.move_line_ids.filtered(
                lambda x: x.lot_id and x.state == "done"
            ):
                cond = [
                    ("sale_order_id", "=", picking.devolution_sale_order_id.id),
                    ("lot_id", "=", move_line.lot_id.id),
                    ("product_id", "=", move_line.product_id.id),
                    ("state", "in", ("done", "2binvoiced")),
                    ("move_id", "=", False),
                ]
                repair = self.env["repair.order"].search(cond, limit=1)
                if repair:
                    repair.create_final_move()

    def _create_backorder(self):
        backorders = super()._create_backorder()
        for backorder in backorders:
            backorder.write(
                {
                    "sale_order_id": backorder.backorder_id.sale_order_id.id,
                    "is_repair": backorder.backorder_id.is_repair,
                }
            )
            backorder.sale_order_id = backorder.backorder_id.sale_order_id
        return backorders
