# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    @api.multi
    def write(self, values):
        result = super(AccountInvoiceLine, self).write(values)
        if ("price_unit" in values and values.get("price_unit", False)):
            for line in self.filtered(
                    lambda x: x.invoice_id.type == "in_invoice"):
                product = line.mapped('product_id')
                if line.invoice_id.state in ("draft", "cancel"):
                    product.set_product_last_supplier_invoice()
                else:
                    product.set_product_last_supplier_invoice(
                        line.invoice_id.id)
        return result
