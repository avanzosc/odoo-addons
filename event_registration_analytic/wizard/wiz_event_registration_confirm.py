# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizEventRegistrationConfirm(models.TransientModel):
    _inherit = 'wiz.event.registration.confirm'

    @api.multi
    def action_confirm_registrations(self):
        registration_obj = self.env['event.registration']
        append_obj = self.env['wiz.event.append.assistant']
        res = super(WizEventRegistrationConfirm,
                    self).action_confirm_registrations()
        for reg in registration_obj.browse(
            self.env.context.get('active_ids')).filtered(
                lambda x: x.state not in ('cancel', 'done') and
                not x.analytic_account and not x.partner_id.employee_id and not
                x.event_id.sale_order.project_id.recurring_invoices):
            append_obj._create_account_for_not_employee_from_wizard(
                reg.event_id, reg)
        return res

    def _prepare_data_confirm_assistant(self, reg):
        append_vals = super(WizEventRegistrationConfirm,
                            self)._prepare_data_confirm_assistant(reg)
        append_vals['create_account'] = True
        sale_order = reg.event_id.sale_order
        if (reg.partner_id.employee_id or reg.analytic_account or
                sale_order.project_id.recurring_invoices):
            append_vals['create_account'] = False
        return append_vals
