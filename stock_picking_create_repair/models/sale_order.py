# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_repair = fields.Boolean(
        string="Is repair", related="type_id.is_repair", store=True, copy=False
    )
    repair_ids = fields.One2many(
        string="Repairs",
        comodel_name="repair.order",
        inverse_name="sale_order_id",
        copy=False,
    )
    repairs_count = fields.Integer(
        string="# Repairs", compute="_compute_repairs_count", copy=False, store=True
    )
    count_in_picking_repairs = fields.Integer(
        string="# Repair in pickings", compute="_compute_count_in_picking_repairs"
    )
    count_out_picking_repairs = fields.Integer(
        string="# Repair out pickings", compute="_compute_count_out_picking_repairs"
    )
    repair_devolution_picking_ids = fields.One2many(
        string="Picking from devolutions",
        comodel_name="stock.picking",
        inverse_name="devolution_sale_order_id",
        copy=False,
    )
    count_repair_devolution_picking = fields.Integer(
        string="# Repair devolution pickings",
        compute="_compute_count_repair_devolution_picking",
    )

    repairs_amount_untaxed = fields.Monetary(
        string="Repairs untaxed amount", copy=False
    )
    count_pending_repairs = fields.Integer(
        string="Num. pending repairs", compute="_compute_count_pending_repairs"
    )

    @api.model
    def _default_type_id(self):
        type_obj = self.env["sale.order.type"]
        cond = [
            ("company_id", "=", self.env.company.id),
            ("is_repair", "=", ("sale_order_from_repair" in self.env.context)),
        ]
        sale_type = type_obj.search(cond, limit=1)
        if not sale_type:
            cond = [
                ("company_id", "=", False),
                ("is_repair", "=", ("sale_order_from_repair" in self.env.context)),
            ]
            sale_type = type_obj.search(cond, limit=1)
        return sale_type

    @api.depends("repair_ids")
    def _compute_repairs_count(self):
        for sale in self:
            sale.repairs_count = len(sale.repair_ids)

    def _compute_count_in_picking_repairs(self):
        for sale in self:
            pickings = sale._search_pickings_repair(
                sale.type_id.picking_type_repair_in_id
            )
            sale.count_in_picking_repairs = len(pickings)

    def _compute_count_out_picking_repairs(self):
        for sale in self:
            pickings = sale._search_pickings_repair(
                sale.type_id.picking_type_repair_out_id
            )
            sale.count_out_picking_repairs = len(pickings)

    def _compute_count_repair_devolution_picking(self):
        for sale in self:
            sale.count_repair_devolution_picking = len(
                sale.repair_devolution_picking_ids
            )

    def _compute_count_pending_repairs(self):
        for sale in self:
            count = 0
            if sale.repair_ids:
                repairs = sale.repair_ids.filtered(
                    lambda x: not x.invoice_id
                    and x.invoice_method != "none"
                    and x.state in ("done", "2binvoiced")
                )
                count = len(repairs)
            sale.count_pending_repairs = count

    def action_devolution_picking_repairs_from_sale(self):
        self.ensure_one()
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.repair_devolution_picking_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_in_picking_repairs_from_sale(self):
        self.ensure_one()
        pickings = self._search_pickings_repair(self.type_id.picking_type_repair_in_id)
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", pickings.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_out_picking_repairs_from_sale(self):
        self.ensure_one()
        pickings = self._search_pickings_repair(self.type_id.picking_type_repair_out_id)
        action = self.env.ref("stock.stock_picking_action_picking_type")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", pickings.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def action_repairs_from_sale(self):
        self.ensure_one()
        action = self.env.ref("repair.action_repair_order_tree")
        action_dict = action.read()[0] if action else {}
        domain = expression.AND(
            [
                [("id", "in", self.repair_ids.ids)],
                safe_eval(action.domain or "[]"),
            ]
        )
        action_dict.update({"domain": domain})
        return action_dict

    def _search_pickings_repair(self, picking_type):
        cond = [
            ("picking_type_id", "=", picking_type.id),
            ("location_id", "=", picking_type.default_location_src_id.id),
            ("location_dest_id", "=", picking_type.default_location_dest_id.id),
            ("partner_id", "=", self.partner_id.id),
            ("sale_order_id", "=", self.id),
            ("company_id", "=", self.company_id.id),
            ("is_repair", "=", True),
        ]
        pickings = self.env["stock.picking"].search(cond)
        return pickings

    def _search_devolution_pickings_repair(self, picking_type):
        cond = [
            ("picking_type_id.code", "=", "incoming"),
            ("partner_id", "=", self.partner_id.id),
            ("sale_order_id", "=", self.id),
            ("company_id", "=", self.company_id.id),
            ("is_repair", "=", True),
        ]
        pickings = self.env["stock.picking"].search(cond)
        return pickings

    def action_create_in_picking_repair_from_sale_order(self):
        self._control_data_ok_for_repair()
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            if lines:
                picking = sale.create_in_picking_repair()
            for line in lines:
                line.create_stock_move_for_in_picking_repair(picking)

    def _control_data_ok_for_repair(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            if lines and not sale.is_repair:
                raise UserError(
                    _(
                        "There are lines with products to be repaired, and the "
                        "type of sale is not repair."
                    )
                )
            if not lines and sale.is_repair:
                raise UserError(
                    _(
                        "The type of sale is repair, and there is no line in "
                        "the sales order with product to be repaired."
                    )
                )
            lines = sale.order_line.filtered(
                lambda x: x.is_repair and not x.product_to_repair_id
            )
            for line in lines:
                raise UserError(
                    _(
                        "You must enter the product to be repaired for product: {}"
                    ).format(line.product_id.name)
                )

    def action_confirm(self):
        result = super().action_confirm()
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.is_repair)
            for line in lines:
                line.initial_price_unit = line.price_unit
        return result

    def create_in_picking_repair(self):
        vals = self._catch_data_for_create_in_picking_repair()
        picking = self.env["stock.picking"].create(vals)
        return picking

    def _catch_data_for_create_in_picking_repair(self):
        picking_type = self.type_id.picking_type_repair_in_id
        vals = {
            "picking_type_id": picking_type.id,
            "location_id": picking_type.default_location_src_id.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
            "partner_id": self.partner_id.id,
            "origin": self.name,
            "sale_order_id": self.id,
            "company_id": self.company_id.id,
            "is_repair": True,
        }
        return vals

    # def ir_cron_put_invoice_in_repair_form_sale_repair(self):
    #     cond = [("is_repair" , "=", True)]
    #     sales = self.env["sale.order"].search(cond)
    #     for sale in sales:
    #         if sale.invoice_count == 1:
    #             repairs = sale.repair_ids.filtered(
    #                 lambda x: x.state in ("done", "2binvoiced") and not
    #                 x.invoice_id)
    #             if repairs:
    #                 repairs.write({"invoice_id": sale.invoice_ids[0].id,
    #                                "state": "done",
    #                                "invoiced": True})
