# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api, exceptions, _


class WizEventAppendAssistant(models.TransientModel):
    _inherit = 'wiz.event.append.assistant'

    show_create_account = fields.Boolean(
        'Show create account', default=False)
    create_account = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')], string='Create Account')

    @api.onchange('partner')
    def onchange_partner(self):
        self.show_create_account = False
        if self.partner:
            event = self.env['event.event'].browse(
                self.env.context.get('active_id'))
            if not event.project_id:
                raise exceptions.Warning(
                    _('You must define a project in event'))
            if not event.project_id.analytic_account_id:
                raise exceptions.Warning(
                    _('The project defined in the event, not associated to an '
                      'analytical account'))
            if not event.project_id.analytic_account_id.recurring_invoices:
                registration = event.registration_ids.filtered(
                    lambda x: x.partner_id.id == self.partner.id and
                    x.analytic_account)
                if not registration:
                    self.show_create_account = True

    @api.multi
    def action_append(self):
        self.ensure_one()
        account_obj = self.env['account.analytic.account']
        event_obj = self.env['event.event']
        if self.show_create_account and not self.create_account:
            raise exceptions.Warning(
                _('You must enter if you want to create account for partner '
                  'registration'))
        result = super(WizEventAppendAssistant, self).action_append()
        if self.create_account:
            for event in event_obj.browse(self.env.context.get('active_ids')):
                registration = event.registration_ids.filtered(
                    lambda x: x.partner_id.id == self.partner.id and not
                    x.analytic_account)
                if registration:
                    code = self.env['ir.sequence'].get(
                        'account.analytic.account')
                    vals = {'name': (_('Event: %s Registration Partner %s') %
                                     (event.name,
                                      registration.partner_id.name)),
                            'type': 'normal',
                            'date_start': self.from_date,
                            'date': self.to_date,
                            'parent_id':
                            event.project_id.analytic_account_id.id,
                            'code': code,
                            'partner_id': registration.partner_id.id}
                    new_account = account_obj.create(vals)
                    registration.analytic_account = new_account.id
        return result
