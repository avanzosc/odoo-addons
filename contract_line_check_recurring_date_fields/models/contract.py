from odoo import api, models


class Contract(models.Model):
    _inherit = "contract.contract"

    @api.onchange("date_start")
    def _onchange_date_start(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.date_start = self.date_start

    @api.onchange("date_end")
    def _onchange_date_end(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.date_end = self.date_end

    @api.onchange("is_terminated")
    def _onchange_is_terminated(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.is_terminated = self.is_terminated

    @api.onchange("terminate_date")
    def _onchange_terminate_date(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.terminate_date = self.terminate_date

    @api.onchange("last_date_invoiced")
    def _onchange_last_date_invoiced(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.last_date_invoiced = self.last_date_invoiced

    @api.onchange("recurring_interval")
    def _onchange_recurring_interval(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.recurring_interval = self.recurring_interval

    @api.onchange("next_period_date_start")
    def _onchange_next_period_date_start(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.next_period_date_start = self.next_period_date_start

    @api.onchange("next_period_date_end")
    def _onchange_next_period_date_end(self):
        if not self.line_recurrence:
            for line in self.contract_line_ids:
                line.next_period_date_end = self.next_period_date_end
