# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import pytz

from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    created_from_move_line_id = fields.Many2one(
        string="Created from detailed operation",
        copy=False,
        comodel_name="stock.move.line",
    )
    created_from_picking_id = fields.Many2one(
        string="Created from incoming picking",
        comodel_name="stock.picking",
        related="created_from_move_line_id.picking_id",
        store=True,
        copy=False,
    )
    purchase_order_id = fields.Many2one(
        string="Purchase order", comodel_name="purchase.order", copy=False
    )
    sale_order_id = fields.Many2one(
        string="Sale order", comodel_name="sale.order", copy=False
    )
    sale_line_id = fields.Many2one(
        string="Sale line",
        comodel_name="sale.order.line",
        related="created_from_move_line_id.sale_line_id",
        store=True,
        copy=False,
    )
    from_repair_picking_out_id = fields.Many2one(
        string="From repair picking out",
        comodel_name="stock.picking",
        copy=False,
        index=True,
    )
    price_in_sale_budget = fields.Float(
        string="Price in sale budget", digits="Product Price", default=0.0, copy=False
    )
    is_repair = fields.Boolean(
        string="Is repair", compute="_compute_is_repair", store=True, copy=False
    )
    commitment_date = fields.Date(
        string="Order Delivery Date",
        compute="_compute_commitment_date",
        store=True,
        copy=False,
    )
    deadline_delivery = fields.Date(
        string="Repair start date", default=False, copy=False
    )
    line_color = fields.Char(
        string="Line color", compute="_compute_line_color", store=True, copy=False
    )

    @api.depends("sale_order_id", "sale_order_id.commitment_date")
    def _compute_commitment_date(self):
        timezone = pytz.timezone(self.env.user.tz or "UTC")
        for repair in self:
            commitment_date = False
            if repair.sale_order_id and repair.sale_order_id.commitment_date:
                commitment_date = (
                    repair.sale_order_id.commitment_date.replace(
                        tzinfo=pytz.timezone("UTC")
                    )
                    .astimezone(timezone)
                    .date()
                )
            repair.commitment_date = commitment_date

    @api.depends("sale_order_id", "sale_order_id.commitment_date", "deadline_delivery")
    def _compute_line_color(self):
        timezone = pytz.timezone(self.env.user.tz or "UTC")
        for repair in self:
            line_color = "None"
            if (
                repair.sale_order_id
                and repair.sale_order_id.commitment_date
                and repair.deadline_delivery
            ):
                commitment_date = (
                    repair.sale_order_id.commitment_date.replace(
                        tzinfo=pytz.timezone("UTC")
                    )
                    .astimezone(timezone)
                    .date()
                )
                if commitment_date < repair.deadline_delivery:
                    line_color = "green"
                else:
                    line_color = "red"
            repair.line_color = line_color

    @api.depends("sale_order_id", "sale_order_id.is_repair")
    def _compute_is_repair(self):
        for repair in self:
            repair.is_repair = (
                repair.sale_order_id.is_repair if repair.sale_order_id else False
            )

    def action_repair_end(self):
        result = super().action_repair_end()
        for repair in self:
            repair.price_in_sale_budget = repair.amount_untaxed
        for repair in self.filtered(lambda r: r.sale_order_id):
            repair.create_out_picking_repair()
        return result

    def create_out_picking_repair(self):
        cond = [
            ("sale_order_id", "=", self.sale_order_id.id),
            ("from_repair_picking_out_id", "!=", False),
            (
                "from_repair_picking_out_id.state",
                "in",
                ["draft", "confirmed", "waiting", "partially_available", "assigned"],
            ),
        ]
        repair = self.env["repair.order"].search(cond)
        if repair:
            picking = repair.from_repair_picking_out_id[:1]
        else:
            vals = self._catch_data_for_create_out_picking_repair()
            picking = self.env["stock.picking"].create(vals)
        lots = self.sale_order_id.mapped("repair_ids.move_id.lot_ids")
        if self.move_id:
            new_move = self.move_id.find_or_create_from_repair(picking)
            new_move.with_context(force_lots=lots)._action_assign()
        self.from_repair_picking_out_id = picking.id

    def _catch_data_for_create_out_picking_repair(self):
        picking_type = self.sale_order_id.type_id.picking_type_repair_out_id
        vals = {
            "picking_type_id": picking_type.id,
            "location_id": picking_type.default_location_src_id.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
            "partner_id": self.sale_order_id.partner_id.id,
            "origin": self.sale_order_id.name,
            "sale_order_id": self.sale_order_id.id,
            "company_id": self.sale_order_id.company_id.id,
            "is_repair": True,
        }
        return vals

    def write(self, values):
        result = super().write(values)
        if "price_in_sale_budget" in values:
            self._put_price_bugdet_in_sale_order_line()
        return result

    def _put_price_bugdet_in_sale_order_line(self):
        for repair in self.filtered(
            lambda x: x.sale_order_id
            and x.created_from_picking_id
            and x.created_from_move_line_id
        ):
            cond = [
                ("sale_order_id", "=", repair.sale_order_id.id),
                ("created_from_picking_id", "=", repair.created_from_picking_id.id),
                ("product_id", "=", repair.product_id.id),
                ("invoice_method", "!=", "none"),
            ]
            for_product_repairs = self.env["repair.order"].search(cond)
            if for_product_repairs:
                price_unit = 0
                price_in_sale_budget = sum(
                    for_product_repairs.mapped("price_in_sale_budget")
                )
                sale_line = repair.created_from_move_line_id.move_id.sale_line_id
                if price_in_sale_budget and sale_line and sale_line.product_uom_qty:
                    price_unit = price_in_sale_budget / sale_line.product_uom_qty
                sale_line.write(
                    {
                        "price_unit": price_unit,
                        "repair_price_in_sale_budget": price_in_sale_budget,
                    }
                )

    def control_action_repair_start(self):
        repairs = self.filtered(lambda r: r.state in ["confirmed", "ready"])
        for repair in repairs:
            repair.action_repair_start()

    def control_action_repair_end(self):
        repairs = self.filtered(lambda r: r.state == "under_repair")
        for repair in repairs:
            repair.action_repair_end()

    def control_action_validate(self):
        repairs = self.filtered(lambda r: r.state == "draft")
        for repair in repairs:
            repair.action_validate()

    def create_final_move(self):
        location = self.from_repair_picking_out_id.location_id
        location_dest = self.from_repair_picking_out_id.location_dest_id
        move = self.env["stock.move"].create(
            {
                "name": self.name,
                "product_id": self.product_id.id,
                "product_uom": self.product_uom.id or self.product_id.uom_id.id,
                "product_uom_qty": self.product_qty,
                "partner_id": self.address_id.id,
                "location_id": location.id,
                "location_dest_id": location_dest.id,
                "repair_id": self.id,
                "origin": self.name,
                "company_id": self.company_id.id,
                "picking_id": self.from_repair_picking_out_id.id,
                "sale_line_id": self.sale_line_id.id,
            }
        )
        #        move.move_line_ids[0]._onchange_serial_number()
        self.move_id = move.id
