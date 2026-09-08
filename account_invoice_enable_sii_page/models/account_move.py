# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends(
        "company_id",
        "company_id.sii_enabled",
        "company_id.sii_start_date",
        "journal_id",
        "journal_id.sii_enabled",
        "move_type",
        "fiscal_position_id",
        "fiscal_position_id.aeat_active",
        "date",
        "invoice_line_ids",
    )
    def _compute_sii_enabled(self):
        result = super()._compute_sii_enabled
        for invoice in self:
            if (
                invoice.company_id.sii_enabled
                and invoice.journal_id.sii_enabled
                and invoice.is_invoice()
            ):
                invoice.sii_enabled = (
                    (
                        invoice.fiscal_position_id
                        and invoice.fiscal_position_id.aeat_active
                    )
                    or not invoice.fiscal_position_id
                ) and (
                    not invoice.company_id.sii_start_date
                    or not invoice.date
                    or invoice.date >= invoice.company_id.sii_start_date
                )
            else:
                invoice.sii_enabled = False
        return result
