# Copyright 2021 Berezi - Iker - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    date = fields.Datetime(string='Date')
    date_end = fields.Datetime(string='Date end')

    @api.multi
    def _compute_duration(self):
        self.ensure_one()
        hours = 0
        minutes = 0
        duration = self.date_end - self.date
        days = duration.days
        seconds = duration.seconds + days * 24 * 3600
        if seconds >= 3600:
            hours = divmod(seconds, 3600)[0]
            seconds = seconds - (hours * 3600)
        if seconds >= 60:
            minutes = divmod(seconds, 60)[0]
            seconds = seconds - (minutes * 60)
        return float('{}.{}'.format(hours, minutes))

    @api.onchange("date", "date_end")
    def onchange_dates(self):
        if self.date:
            if self.date_end:
                self.unit_amount = self._compute_duration()

    @api.multi
    def action_button_end(self):
        self.ensure_one()
        for line in self:
            line.date_end = fields.Datetime.now()
            line.unit_amount = self._compute_duration()
