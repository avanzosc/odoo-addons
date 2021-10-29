# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ContractContract(models.Model):
    _inherit = 'contract.contract'

    def _prepare_invoice(self, date_invoice, journal=None):
        contract_lines = self._get_lines_to_invoice(date_invoice)
        line_min_fec = min(
            contract_lines, key=lambda x: x.next_period_date_start)
        line_max_fec = min(
            contract_lines, key=lambda x: x.next_period_date_end)
        invoice_vals, move_form = super(
            ContractContract, self)._prepare_invoice(
                date_invoice, journal=journal)
        invoice_vals.update(
            {'start_date_period': line_min_fec.next_period_date_start,
             'end_date_period': line_max_fec.next_period_date_end})
        return invoice_vals, move_form
