# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_repair = fields.Boolean(
        string="Is repair", related="product_id.is_repair", store=True, copy=False
    )
    product_to_repair_id = fields.Many2one(
        string="Product to repair", comodel_name="product.product", copy=False
    )
    initial_price_unit = fields.Float(
        string="Initial price unit", digits="Product Price", default=0.0, copy=False
    )
    repair_amount_untaxed = fields.Monetary(
        string="Repair untaxed amount",
        copy=False,
        store=True,
        compute="_compute_repair_amount_untaxed",
    )
    repair_price_in_sale_budget = fields.Float(
        string="Repairs price in sale budget",
        digits="Product Price",
        default=0.0,
        copy=False,
    )
    repair_order_ids = fields.One2many(
        string="Repair orders",
        comodel_name="repair.order",
        inverse_name="sale_line_id",
        copy=False,
    )
    repair_picking_move_line_ids = fields.One2many(
        string="Stock move lines from repair pickings",
        copy=False,
        comodel_name="stock.move.line",
        inverse_name="sale_line_id",
    )
    service_repair_product_id = fields.Many2one(
        string="Service repair product", comodel_name="product.product", copy=False
    )

    @api.depends(
        "repair_order_ids",
        "repair_order_ids.amount_untaxed",
        "repair_order_ids.invoice_method",
        "repair_order_ids.state",
    )
    def _compute_repair_amount_untaxed(self):
        for line in self:
            repair_amount_untaxed = 0
            if line.is_service and line.is_repair and line.product_to_repair_id:
                repairs = line.repair_order_ids.filtered(
                    lambda x: x.invoice_method != "none" and x.state != "cancel"
                )
                if repairs:
                    repair_amount_untaxed = sum(repairs.mapped("amount_untaxed"))
            line.repair_amount_untaxed = repair_amount_untaxed

    @api.onchange("product_id")
    def product_id_change(self):
        warning = {}
        result = super().product_id_change()
        if self.product_id and self.product_id.is_repair:
            lit_message = _("You must enter the product to repair")
            if "warning" not in result:
                warning["title"] = _("Warning for %s", self.product_id.name)
                warning["message"] = lit_message
                result = {"warning": warning}
            else:
                warning = result.get("warning")
                my_message = "{} \n {}".format(warning.get("message"), lit_message)
                result["warning"]["message"] = my_message
        return result

    def create_stock_move_for_in_picking_repair(self, picking):
        vals = self._catch_data_for_create_move_in_picking_repair(picking)
        self.env["stock.move"].create(vals)

    def _catch_data_for_create_move_in_picking_repair(self, picking):
        vals = {
            "name": self.product_to_repair_id.name,
            "product_id": self.product_to_repair_id.id,
            "partner_id": self.order_id.partner_id.id,
            "location_id": picking.location_id.id,
            "location_dest_id": picking.location_dest_id.id,
            "picking_id": picking.id,
            "sale_line_id": self.id,
            "company_id": self.order_id.company_id.id,
            "picking_type_id": picking.picking_type_id.id,
            "origin": self.order_id.name,
            "description_picking": self.product_to_repair_id.name,
            "propagate_cancel": True,
            "warehouse_id": picking.picking_type_id.warehouse_id.id,
            "product_uom_qty": self.product_uom_qty,
            "product_uom": self.product_to_repair_id.uom_po_id.id,
        }
        return vals

    def _prepare_invoice_line(self, **optional_values):
        self.ensure_one()
        values = super()._prepare_invoice_line(**optional_values)
        repairs = self.repair_order_ids.filtered(
            lambda x: not x.invoice_id
            and x.state in ("done", "2binvoiced")
            and x.invoice_method != "none"
        )
        if repairs:
            qty = sum(repairs.mapped("product_qty"))
            amount_untaxed = sum(repairs.mapped("amount_untaxed"))
            price_unit = amount_untaxed / qty
            values["quantity"] = qty
            values["price_unit"] = price_unit
        return values

    def get_rma_to_print(self):
        repairs = ""
        for repair in self.repair_order_ids:
            repairs = (
                repair.name if not repairs else "{}, {}".format(repairs, repair.name)
            )
        return repairs

    @api.depends(
        "product_uom_qty",
        "qty_delivered_method",
        "qty_delivered",
        "price_unit",
        "discount",
        "repair_order_ids",
        "repair_order_ids.state",
        "repair_order_ids.from_repair_picking_out_id",
        "repair_picking_move_line_ids",
        "repair_picking_move_line_ids.state",
        "repair_picking_move_line_ids.lot_id",
    )
    def _compute_qty_amount_pending_delivery(self):
        result = True
        for line in self:
            if (
                line.is_service
                and line.is_repair
                and line.product_to_repair_id
                and line.order_id.is_repair
            ):
                qty_pending_delivery = line.product_uom_qty - line.qty_delivered
                if qty_pending_delivery < 0:
                    qty_pending_delivery = 0
                line.qty_pending_delivery = qty_pending_delivery
                line.amount_pending_delivery = line._get_amount_pending_delivery()
            else:
                result = super(
                    SaleOrderLine, line
                )._compute_qty_amount_pending_delivery()
        return result

    def _get_amount_pending_delivery(self):
        amount_pending_delivery = 0
        for repair in self.repair_order_ids.filtered(lambda x: x.state != "cancel"):
            if not repair.from_repair_picking_out_id:
                amount_pending_delivery += repair.amount_untaxed
            else:
                move_lines = self.repair_picking_move_line_ids.filtered(
                    lambda x: x.lot_id == repair.lot_id
                    and x.picking_id == repair.from_repair_picking_out_id
                )
                if not move_lines:
                    amount_pending_delivery += repair.amount_untaxed
                else:
                    move_lines = move_lines.filtered(
                        lambda z: z.state not in ("done", "cancel")
                    )
                    if move_lines:
                        amount_pending_delivery += repair.amount_untaxed
        return amount_pending_delivery

    @api.depends(
        "qty_delivered",
        "qty_invoiced",
        "discount",
        "price_unit",
        "repair_order_ids",
        "repair_order_ids.state",
        "repair_order_ids.amount_untaxed",
        "repair_order_ids.invoice_method",
        "repair_order_ids.from_repair_picking_out_id",
        "repair_order_ids.invoice_id",
        "repair_picking_move_line_ids",
        "repair_picking_move_line_ids.state",
        "repair_picking_move_line_ids.lot_id",
    )
    def _compute_qty_shipped_pending_invoicing(self):
        result = True
        for line in self:
            if (
                line.is_service
                and line.is_repair
                and line.product_to_repair_id
                and line.order_id.is_repair
            ):
                amount = 0
                qty = 0
                if line.repair_order_ids:
                    amount, qty = line._get_info_shipped_pending_invoicing()
                line.amount_shipped_pending_invoicing = amount
                line.qty_shipped_pending_invoicing = qty
            else:
                result = super(
                    SaleOrderLine, line
                )._compute_qty_amount_pending_delivery()
        return result

    def _get_info_shipped_pending_invoicing(self):
        amount = 0
        qty = 0
        for repair in self.repair_order_ids.filtered(
            lambda x: x.state != "cancel"
            and x.from_repair_picking_out_id
            and x.invoice_method != "none"
            and not x.invoice_id
        ):
            move_lines = self.repair_picking_move_line_ids.filtered(
                lambda z: z.picking_id == repair.from_repair_picking_out_id
                and z.sale_line_id == repair.sale_line_id
                and z.lot_id == repair.lot_id
                and z.state == "done"
            )
            if move_lines:
                amount += repair.amount_untaxed
                qty += repair.product_qty
        return amount, qty

    @api.depends(
        "product_uom_qty",
        "qty_invoiced",
        "discount",
        "price_unit",
        "repair_order_ids",
        "repair_order_ids.amount_untaxed",
        "repair_order_ids.invoice_method",
        "repair_order_ids.state",
        "repair_order_ids.invoice_id",
        "repair_order_ids.invoice_id.state",
        "repair_order_ids.invoice_id.amount_residual",
    )
    def _compute_qty_amount_pending_invoicing(self):
        result = True
        for line in self:
            if (
                line.is_service
                and line.is_repair
                and line.product_to_repair_id
                and line.order_id.is_repair
            ):
                line.qty_pending_invoicing = line.product_uom_qty - line.qty_invoiced
                if not line.repair_order_ids:
                    amount = line.qty_pending_invoicing * line.price_unit
                else:
                    amount = line._get_amount_pending_invoicing()
                line.amount_pending_invoicing = amount
            else:
                result = super(
                    SaleOrderLine, line
                )._compute_qty_amount_pending_invoicing()
        return result

    def _get_amount_pending_invoicing(self):
        amount = 0
        repairs_without_invoice = self.repair_order_ids.filtered(
            lambda x: not x.invoice_id
            and x.state != "cancel"
            and x.invoice_method != "none"
        )
        if repairs_without_invoice:
            amount += sum(repairs_without_invoice.mapped("amount_untaxed"))
        return amount

    @api.depends(
        "move_ids.state",
        "move_ids.scrapped",
        "move_ids.product_uom_qty",
        "move_ids.product_uom",
    )
    def _compute_qty_delivered(self):
        my_lines = self.env["sale.order.line"]
        for line in self.filtered(
            lambda x: x.is_service and x.is_repair and x.product_to_repair_id
        ):
            line.write(
                {
                    "service_repair_product_id": line.product_id.id,
                    "product_id": line.product_to_repair_id.id,
                }
            )
            line._compute_qty_delivered_method()
            my_lines += line
        result = super()._compute_qty_delivered()
        for line in my_lines:
            line.write(
                {
                    "is_service": True,
                    "is_repair": True,
                    "product_id": line.service_repair_product_id.id,
                    "service_repair_product_id": False,
                }
            )
            line._compute_qty_delivered_method()
        return result

    @api.onchange("qty_delivered")
    def _inverse_qty_delivered(self):
        my_lines = self.env["sale.order.line"]
        for line in self.filtered(
            lambda x: x.is_service and x.is_repair and x.product_to_repair_id
        ):
            line.write(
                {
                    "service_repair_product_id": line.product_id.id,
                    "product_id": line.product_to_repair_id.id,
                }
            )
            line._compute_qty_delivered_method()
            my_lines += line
        result = super()._inverse_qty_delivered()
        for line in my_lines:
            line.write(
                {
                    "is_service": True,
                    "is_repair": True,
                    "product_id": line.service_repair_product_id.id,
                    "service_repair_product_id": False,
                }
            )
            line._compute_qty_delivered_method()
        return result
