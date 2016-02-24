# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _prepare_event_data(self, project):
        res = super(SaleOrder, self)._prepare_event_data(project)
        if self.project_id.date_start:
            time = self.project_id.start_time or 0
            utc_dt = self._put_utc_format_date(self.project_id.date_start,
                                               time)
            res['date_begin'] = utc_dt
        if self.project_id.date:
            time = self.project_id.end_time or 0
            utc_dt = self._put_utc_format_date(self.project_id.date, time)
            res['date_end'] = utc_dt
        return res

    def _prepare_session_data_from_sale_line(
            self, event, num_session, line, date):
        vals = super(SaleOrder, self)._prepare_session_data_from_sale_line(
            event, num_session, line, date)
        time = self.project_id.start_time or 0
        vals['date'] = self._put_utc_format_date(date, time)
        return vals
