# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class WizRegistrationToAnotherEvent(models.TransientModel):
    _inherit = 'wiz.registration.to.another.event'

    def _change_registration_event(self, registration):
        wiz_append_obj = self.env['wiz.event.append.assistant']
        super(WizRegistrationToAnotherEvent, self)._change_registration_event(
            registration)
        if registration.analytic_account:
            vals = wiz_append_obj._prepare_data_for_account_not_employee(
                self.new_event_id, registration)
            vals.pop('code', False)
            vals.pop('date', False)
            vals.pop('date_start', False)
            vals.pop('recurring_next_date', False)
            registration.analytic_account.write(vals)
