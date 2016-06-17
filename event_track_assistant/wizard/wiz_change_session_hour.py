# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizChangeSessionHour(models.TransientModel):
    _name = 'wiz.change.session.hour'

    new_hour = fields.Float(string='New hour', required=True)

    @api.multi
    def change_session_hour(self):
        self.ensure_one()
        session_obj = self.env['event.track']
        event_obj = self.env['event.event']
        sessions = session_obj.browse(self.env.context.get('active_ids'))
        for session in sessions:
            new_date = event_obj._convert_date_to_local_format_with_hour(
                session.date).date()
            utc_dt = event_obj._put_utc_format_date(new_date, self.new_hour)
            session.date = utc_dt
