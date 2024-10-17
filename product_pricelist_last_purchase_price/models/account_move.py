# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models
from odoo.exceptions import AccessError


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        result = super(AccountMove, self).action_post()
        for invoice in self.filtered(
            lambda x: x.move_type == "in_invoice" and x.state == "posted"
        ):
            invoice._add_supplier_to_product()
        return result

    def _add_supplier_to_product(self):
        for line in self.invoice_line_ids:
            partner = (
                self.partner_id
                if not self.partner_id.parent_id
                else self.partner_id.parent_id
            )
            if (
                line.product_id
                and partner not in line.product_id.seller_ids.mapped("name")
                and len(line.product_id.seller_ids) <= 10
            ):
                currency = (
                    partner.property_purchase_currency_id
                    or self.env.company.currency_id
                )
                price = self.currency_id._convert(
                    line.price_unit,
                    currency,
                    line.company_id,
                    line.move_id.invoice_date or fields.Date.today(),
                    round=False,
                )
                if line.product_id.product_tmpl_id.uom_po_id != line.product_uom_id:
                    default_uom = line.product_id.product_tmpl_id.uom_po_id
                    price = line.product_uom_id._compute_price(price, default_uom)
                sellers = line.product_id.seller_ids
                supplierinfo = {
                    "name": partner.id,
                    "sequence": max(sellers.mapped("sequence")) + 1 if sellers else 1,
                    "min_qty": 0.0,
                    "price": price,
                    "currency_id": currency.id,
                    "delay": 0,
                }
                seller = line.product_id._select_seller(
                    partner_id=line.move_id.partner_id,
                    quantity=line.quantity,
                    date=line.move_id.invoice_date,
                    uom_id=line.product_uom_id,
                )
                if seller:
                    supplierinfo["product_name"] = seller.product_name
                    supplierinfo["product_code"] = seller.product_code
                vals = {
                    "seller_ids": [(0, 0, supplierinfo)],
                }
                try:
                    line.product_id.write(vals)
                except AccessError:
                    break
        self._update_supplier_info_to_product()

    def _update_supplier_info_to_product(self):
        for line in self.invoice_line_ids:
            partner = (
                self.partner_id
                if not self.partner_id.parent_id
                else self.partner_id.parent_id
            )
            seller = self._find_seller_to_update_suppliernfo_to_product(line, partner)
            if seller:
                vals = self._catch_values_to_update_seller_in_product(line, seller)
                seller.write(vals)

    def _catch_values_to_update_seller_in_product(self, line, seller):
        vals = {}
        if seller.price != line.price_unit:
            vals["price"] = line.price_unit
        if seller.discount != line.discount:
            vals["discount"] = line.discount
        return vals

    def _find_seller_to_update_suppliernfo_to_product(self, line, partner):
        seller = line.product_id.seller_ids.filtered(
            lambda x: x.name == partner
            and (x.price != line.price_unit or x.discount != line.discount)
        )
        if seller and seller.not_update_price_from_invoice:
            seller = False
        return seller
