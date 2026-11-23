# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class RepairOrder(models.Model):
    _inherit = "repair.order"

    partner_invoice_id = fields.Many2one(
        string="Invoicing Address", comodel_name="res.partner", check_company=True
    )
    address_id = fields.Many2one(
        string="Delivery Address",
        comodel_name="res.partner",
        domain="[('parent_id','=',partner_id)]",
        check_company=True,
    )
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
    sale_id = fields.Many2one(
        string="Sale order",
        comodel_name="sale.order",
        related="sale_line_id.order_id",
        store=True,
        copy=False,
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
    invoice_id = fields.Many2one(
        string="Invoice",
        comodel_name="account.move",
    )
    currency_id = fields.Many2one(
        string="Currency",
        comodel_name="res.currency",
        copy=False,
        store=True,
        related="invoice_id.currency_id",
    )
    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        copy=False,
        store=True,
        currency_field="currency_id",
        related="invoice_id.amount_untaxed",
    )
    company_currency_id = fields.Many2one(
        string="Company Currency", related="company_id.currency_id"
    )
    lines_amount_untaxed = fields.Monetary(
        string="Tax Base",
        currency_field="company_currency_id",
        compute="_compute_lines_amounts",
        store=True,
    )
    lines_amount_tax = fields.Monetary(
        string="Taxes",
        currency_field="company_currency_id",
        compute="_compute_lines_amounts",
        store=True,
    )
    lines_amount_total = fields.Monetary(
        string="Total",
        currency_field="company_currency_id",
        compute="_compute_lines_amounts",
        store=True,
    )

    @api.depends(
        "move_ids.price_subtotal",
        "move_ids.price_tax",
        "move_ids.repair_line_type",
        "move_ids.state",
        "repair_service_ids.price_subtotal",
        "repair_service_ids.price_tax",
    )
    def _compute_lines_amounts(self):
        for repair in self:
            lines = repair.move_ids.filtered(
                lambda x: x.repair_line_type == "add" and x.state != "cancel"
            )
            services = repair.repair_service_ids
            untaxed = sum(lines.mapped("price_subtotal")) + sum(
                services.mapped("price_subtotal")
            )
            tax = sum(lines.mapped("price_tax")) + sum(services.mapped("price_tax"))
            repair.lines_amount_untaxed = untaxed
            repair.lines_amount_tax = tax
            repair.lines_amount_total = untaxed + tax

    def _get_repair_product_taxes(self, product):
        self.ensure_one()
        taxes = product.taxes_id._filter_taxes_by_company(self.company_id)
        if not taxes or not self.partner_id:
            return taxes
        fiscal_position = (
            self.env["account.fiscal.position"]
            .with_company(self.company_id)
            ._get_fiscal_position(
                self.partner_id, delivery=self.address_id or self.partner_id
            )
        )
        return fiscal_position.map_tax(taxes)

    @api.depends("sale_id", "sale_id.is_repair")
    def _compute_is_repair(self):
        for repair in self:
            repair.is_repair = repair.sale_id.is_repair if repair.sale_id else False

    def _put_amount_untaxed_in_price_in_sale_budget(self):
        for repair in self.filtered(
            lambda x: x.state == "draft" and x.sale_id and x.sale_id.is_repair
        ):
            repair.price_in_sale_budget = repair.lines_amount_untaxed

    def action_repair_end(self):
        result = super().action_repair_end()
        for repair in self:
            repair.price_in_sale_budget = repair.lines_amount_untaxed
        for repair in self.filtered(lambda r: r.sale_id):
            repair.create_out_picking_repair()
        return result

    def create_out_picking_repair(self):
        cond = [
            ("sale_id", "=", self.sale_id.id),
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
        lots = self.sale_id.mapped("repair_ids.move_id.lot_ids")
        if self.move_id:
            new_move = self.move_id.find_or_create_from_repair(picking)
            new_move.with_context(force_lots=lots)._action_assign()
        self.from_repair_picking_out_id = picking.id

    def _catch_data_for_create_out_picking_repair(self):
        picking_type = self.sale_id.type_id.picking_type_repair_out_id
        vals = {
            "picking_type_id": picking_type.id,
            "location_id": picking_type.default_location_src_id.id,
            "location_dest_id": picking_type.default_location_dest_id.id,
            "partner_id": self.address_id.id or self.sale_id.partner_shipping_id.id,
            "origin": self.sale_id.name,
            "sale_order_id": self.sale_id.id,
            "company_id": self.sale_id.company_id.id,
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
            lambda x: x.sale_id
            and x.created_from_picking_id
            and x.created_from_move_line_id
        ):
            cond = [
                ("sale_id", "=", repair.sale_id.id),
                ("created_from_picking_id", "=", repair.created_from_picking_id.id),
                ("product_id", "=", repair.product_id.id),
                # ("product_id", "=", repair.product_id.id),
                # ("invoice_method", "!=", "none"),
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
