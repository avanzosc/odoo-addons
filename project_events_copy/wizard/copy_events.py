# -*- coding: utf-8 -*-
# © 2014-2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

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
                    event.project_id.date_start), datetime.min.time())
                diff_days = start - end
                begin = (fields.Datetime.from_string(event.date_begin) +
                         diff_days)
                end = (fields.Datetime.from_string(event.date_end) +
                       diff_days)
                event_dic['date_begin'] = fields.Datetime.to_string(begin)
                event_dic['date_end'] = fields.Datetime.to_string(end)
            event.write(event_dic)
        return {'type': 'ir.actions.act_window_close'}
