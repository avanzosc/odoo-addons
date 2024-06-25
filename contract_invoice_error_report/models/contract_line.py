# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from dateutil.relativedelta import relativedelta

from odoo import _, models


class ContractLine(models.Model):
    _inherit = "contract.line"

    def _prepare_invoice_line_error(self, move_form):
        self.ensure_one()
        self.sudo()._get_period_to_invoice_error(
            self.last_date_invoiced, self.recurring_next_date
        )

    def _get_period_to_invoice_error(
        self, last_date_invoiced, recurring_next_date, stop_at_date_end=True
    ):
        self.ensure_one()
        if not recurring_next_date:
            return False, False, False
            error = _("Contract without recurring next date")
            self.contract_id.sudo().write(
                {
                    "with_invoice_generation_error": True,
                    "invoice_generation_error": error,
                }
            )
            return True
        my_last_date_invoiced = last_date_invoiced
        first_date_invoiced = (
            last_date_invoiced + relativedelta(days=1)
            if last_date_invoiced
            else self.date_start
        )
        if not first_date_invoiced:
            error = _(
                "Contract without first date invoiced. Last date "
                "invoice: {}, Date start: {}. How result without first "
                "date invoiced: {}."
            ).format(my_last_date_invoiced, self.date_start, first_date_invoiced)
            self.contract_id.sudo().write(
                {
                    "with_invoice_generation_error": True,
                    "invoice_generation_error": error,
                }
            )
            return True
        max_date_end = self.date_end if stop_at_date_end else False
        if max_date_end and first_date_invoiced > max_date_end:
            error = _(
                "Next period date start > Max. Date end. Last date "
                "invoice: {}, Date start: {}. How result Next period date "
                "start: {}. Stop at date end: {}, Line date end: {}. How "
                "result Max. Date end: {}."
            ).format(
                my_last_date_invoiced,
                self.date_start,
                first_date_invoiced,
                stop_at_date_end,
                self.date_end,
                max_date_end,
            )
            self.contract_id.sudo().write(
                {
                    "with_invoice_generation_error": True,
                    "invoice_generation_error": error,
                }
            )
