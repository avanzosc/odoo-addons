# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model_create_multi
    def create(self, vals_list):
        key = self.env["tbai.vat.regime.key"].search([("code", "=", "03")], limit=1)
        invoices = super().create(vals_list)
        invoices_rebu = invoices.filtered(
            lambda x: x.move_type
            and x.move_type in ("out_invoice", "out_refund")
            and x.journal_id
            and x.journal_id.is_rebu
        )
        if invoices_rebu:
            invoices_rebu.write({"tbai_vat_regime_key": key.id})
        return invoices

    def tbai_prepare_invoice_values(self):
        values = super().tbai_prepare_invoice_values()
        if not self.is_rebu:
            return values
        tbai_invoice_line_ids = []
        lines = self.invoice_line_ids.filtered(
            lambda c: c.tax_ids and c.price_unit >= 0
        )
        for line in lines:
            description_line = line.name[:250]
            if (
                self.company_id.tbai_protected_data
                and self.company_id.tbai_protected_data_txt
            ):
                description_line = self.company_id.tbai_protected_data_txt[:250]
            tbai_invoice_line_ids.append(
                (
                    0,
                    0,
                    {
                        "description": description_line,
                        "quantity": "%.2f" % line.quantity,
                        "price_unit": "%.8f" % line.price_total,
                        "discount_amount": "0.00",
                        "amount_total": "%.2f" % line.price_total,
                    },
                )
            )
        values["tbai_invoice_line_ids"] = tbai_invoice_line_ids
        return values
