
# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

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
