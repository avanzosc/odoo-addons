# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("requisition_id")
    def _onchange_requisition_id(self):
        if self.requisition_id:
            self = self.with_company(self.company_id)
            requisition = self.requisition_id
            if self.partner_id:
                partner = self.partner_id
            else:
                partner = requisition.vendor_id
            payment_term = partner.property_supplier_payment_term_id
            FiscalPosition = self.env["account.fiscal.position"]
            fpos = FiscalPosition.with_company(self.company_id).get_fiscal_position(
                partner.id
            )
            self.partner_id = partner.id
            self.fiscal_position_id = fpos.id
            self.payment_term_id = (payment_term.id,)
            self.company_id = requisition.company_id.id
            self.currency_id = requisition.currency_id.id
            if not self.origin or requisition.name not in self.origin.split(", "):
                if self.origin:
                    if requisition.name:
                        self.origin = self.origin + ", " + requisition.name
                else:
                    self.origin = requisition.name
            self.notes = requisition.description
            self.date_order = fields.Datetime.now()
            if requisition.type_id.line_copy != "copy":
                return
            order_lines = []
            for line in requisition.line_ids:
                product_lang = line.product_id.with_context(
                    lang=partner.lang or self.env.user.lang, partner_id=partner.id
                )
                name = product_lang.display_name
                if product_lang.description_purchase:
                    name += "\n" + product_lang.description_purchase
                taxes_ids = fpos.map_tax(
                    line.product_id.supplier_taxes_id.filtered(
                        lambda tax: tax.company_id == requisition.company_id
                    )
                ).ids
                if line.product_uom_id != line.product_id.uom_po_id:
                    product_qty = line.product_uom_id._compute_quantity(
                        line.product_qty, line.product_id.uom_po_id
                    )
                    price_unit = line.product_uom_id._compute_price(
                        line.price_unit, line.product_id.uom_po_id
                    )
                else:
                    product_qty = line.product_qty
                    price_unit = line.price_unit
                if requisition.type_id.quantity_copy != "copy":
                    product_qty = 0
                order_line_values = line._prepare_purchase_order_line(
                    name=name,
                    product_qty=product_qty,
                    price_unit=price_unit,
                    taxes_ids=taxes_ids,
                )
                product = date_planned = False
                if "product_id" in order_line_values:
                    product = self.env["product.product"].browse(
                        order_line_values.get("product_id")
                    )
                if "date_planned" in order_line_values:
                    date_planned = order_line_values.get("date_planned").date()
                if product and date_planned:
                    if self.order_line and self.order_line.filtered(
                        lambda c: c.product_id == product
                    ):
                        continue
                    else:
                        order_lines.append((0, 0, order_line_values))
            self.order_line = order_lines
