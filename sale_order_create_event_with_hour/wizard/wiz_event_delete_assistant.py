# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class WizEventDeleteAssistant(models.TransientModel):
    _inherit = 'wiz.event.delete.assistant'

    start_time = fields.Float(string='Start time')
    end_time = fields.Float(string='End time')

    def _prepare_track_condition_from_date(self, sessions):
        from_date = self._put_utc_format_date(
            self.from_date, self.start_time).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '<', from_date)]
        return cond

    def _prepare_track_condition_to_date(self, sessions):
        to_date = self._put_utc_format_date(
            self.to_date, self.end_time).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                ('date', '>', to_date)]
        return cond

    def _prepare_track_search_condition_for_delete(self, sessions):
        from_date = self._put_utc_format_date(
            self.from_date, self.start_time).strftime('%Y-%m-%d %H:%M:%S')
        to_date = self._put_utc_format_date(
            self.to_date, self.end_time).strftime('%Y-%m-%d %H:%M:%S')
        cond = [('id', 'in', sessions.ids),
                '|', ('date', '=', False), '&',
                ('date', '>=', from_date),
                ('date', '<=', to_date)]
        return cond
