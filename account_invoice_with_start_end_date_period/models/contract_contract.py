# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    def _prepare_invoice(self, date_invoice, journal=None):
        contract_lines = self._get_lines_to_invoice(date_invoice)
        line_min_fec = False
        line_max_fec = False
        for line in contract_lines:
            if line.next_period_date_start:
                if not line_min_fec:
                    line_min_fec = line.next_period_date_start
                else:
                    if line.next_period_date_start < line_min_fec:
                        line_min_fec = line.next_period_date_start
            if line.next_period_date_end:
                if not line_max_fec:
                    line_max_fec = line.next_period_date_end
                else:
                    if line.next_period_date_end < line_max_fec:
                        line_max_fec = line.next_period_date_end
        invoice_vals, move_form = super()._prepare_invoice(
            date_invoice, journal=journal
        )
        vals = {}
        if line_min_fec:
            vals["start_date_period"] = line_min_fec
        if line_max_fec:
            vals["end_date_period"] = line_max_fec
        if vals:
            invoice_vals.update(vals)
        print("fffffff salgo")
        return invoice_vals, move_form
