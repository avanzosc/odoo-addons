# -*- coding: utf-8 -*-
# (c) 2016 Mikel Arregi - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, models, fields
from dateutil.relativedelta import relativedelta
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT


class EventsDateModify(models.TransientModel):
    _name = 'events.date.modify'
    _rec_name = 'measure'

    forward = fields.Boolean(string='Forward')
    qty = fields.Integer(string='qty')
    measure = fields.Selection([('days', 'Days'), ('months', 'Months')],
                               string='Measure')

    @api.multi
    def modify_date(self):
        event_obj = self.env['event.event']
        events = event_obj.browse(self.env.context['active_ids'])
        for event in events:
            if self.measure == 'months':
                event.write({
                    'date_begin':
                    datetime.strptime(
                        event.date_begin, DEFAULT_SERVER_DATETIME_FORMAT) +
                    relativedelta(months=(self.forward and -self.qty) or
                                  self.qty),
                    'date_end':
                    datetime.strptime(
                        event.date_end, DEFAULT_SERVER_DATETIME_FORMAT) +
                    relativedelta(months=(self.forward and -self.qty) or
                                  self.qty)})
            else:
                event.write({
                    'date_begin':
                    datetime.strptime(
                        event.date_begin, DEFAULT_SERVER_DATETIME_FORMAT) +
                    relativedelta(days=(self.forward and -self.qty) or
                                  self.qty),
                    'date_end':
                    datetime.strptime(event.date_end,
                                      DEFAULT_SERVER_DATETIME_FORMAT) +
                    relativedelta(days=(self.forward and -self.qty) or
                                  self.qty)})
        return {'type': 'ir.actions.act_window_close'}
