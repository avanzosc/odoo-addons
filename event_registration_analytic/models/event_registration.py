# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    analytic_account = fields.Many2one(
        'account.analytic.account', string='Analytic account')

    @api.multi
    def registration_open(self):
        wiz_obj = self.env['wiz.event.append.assistant']
        result = super(EventRegistration, self).registration_open()
        event = self.env['event.event'].browse(
            result['context'].get('event_id'))
        if not event.project_id:
            raise exceptions.Warning(
                _('You must define a project in event'))
        if not event.project_id.analytic_account_id:
            raise exceptions.Warning(
                _('The project defined in the event, not associated to an '
                  'analytical account'))
        wiz = wiz_obj.browse(result.get('res_id'))
        wiz.show_create_account = False
        if (not event.project_id.analytic_account_id.recurring_invoices and
                not self.analytic_account):
            wiz.show_create_account = True
        return result
