# -*- coding: utf-8 -*-
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class EventsTimeModify(models.TransientModel):
    _name = 'events.time.modify'
    _rec_name = 'start_time'

    start_time = fields.Datetime(string='Start Time')
    qty = fields.Integer(string='qty')

    @api.multi
    def change_time(self):
        event_obj = self.env['event.event']
        events = event_obj.browse(self.env.context['active_ids'])
        for event in events:
            event_date = datetime.combine(
                datetime.strptime(event.date_begin,
                                  DEFAULT_SERVER_DATETIME_FORMAT),
                datetime.strptime(self.start_time,
                                  DEFAULT_SERVER_DATETIME_FORMAT).time())
            event.write({
                'date_begin': event_date,
                'date_end': event_date + relativedelta(hours=self.qty)})
        return {'type': 'ir.actions.act_window_close'}
