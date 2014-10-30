
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

from openerp import models, api, fields
from datetime import datetime


class EventsCopy(models.TransientModel):
    _name = "events.copy"
    _rec_name = "project_id"
    project_id = fields.Many2one('project.project', string="Project")
    start_date = fields.Datetime(string="Start Date")

    @api.multi
    def copy_events(self):
        event_obj = self.env['event.event']
        events = event_obj.browse(self.env.context['active_ids']).copy()
        for event in events:
            event_dic = {'project_id': self.project_id.id}
            if event.project_id.date_start:
                if self.start_date:
                    start = fields.Datetime.from_string(self.start_date)
                else:
                    start = datetime.combine(fields.Date.from_string(
                        self.project_id.date_start), datetime.min.time())
                end = datetime.combine(fields.Date.from_string(
                    event.project_id.date_start, datetime.min.time()))
                diff_days = start - end
                begin = (fields.Datetime.from_string(event.date_begin) +
                         diff_days)
                end = (fields.Datetime.from_string(event.date_end) +
                       diff_days)
                event_dic['date_begin'] = fields.Datetime.to_string(begin)
                event_dic['date_end'] = fields.Datetime.to_string(end)
            event.write(event_dic)
        return {'type': 'ir.actions.act_window_close'}
