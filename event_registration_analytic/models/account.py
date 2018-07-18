# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    student = fields.Many2one(
        comodel_name='res.partner', string='Student')


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    student = fields.Many2one(
        comodel_name='res.partner', string='Student')
    event_id = fields.Many2one(
        comodel_name='event.event', string='Event')
    sale_order_id = fields.Many2one(
        comodel_name='sale.order', string='Sale order')
    event_address_id = fields.Many2one(
        comodel_name='res.partner', string='Event address')

    @api.model
    @api.returns('self', lambda value: value.id)
    def create(self, vals):
        account_obj = self.env['account.analytic.account']
        registration_obj = self.env['event.registration']
        if (vals.get('origin', False) and
                vals.get('type', False) == 'out_invoice'):
            cond = [('code', '=', vals.get('origin'))]
            account = account_obj.search(cond, limit=1)
            if account.sale.payer == 'school':
                vals['journal_id'] = self.env.ref(
                    'event_registration_analytic.school_journal').id
                vals['sale_order_id'] = account.sale.id or False
                vals['event_address_id'] = (
                    account.sale.partner_shipping_id.id or False)
                vals['payment_mode_id'] = (account.sale.payment_mode_id.id or
                                           vals.get('payment_mode_id', False))
            if account.sale.payer == 'student':
                cond = [('analytic_account', '=', account.id)]
                registration = registration_obj.search(cond, limit=1)
                vals['sale_order_id'] = (
                    registration.event_id.sale_order.id or False)
                vals['event_address_id'] = (
                    registration.event_id.address_id.id or False)
                vals['journal_id'] = self.env.ref(
                    'event_registration_analytic.student_journal').id
                vals['student'] = account.student.id
                vals['event_id'] = registration.event_id.id or False
                vals['payment_mode_id'] = (
                    account.student.parent_id.customer_payment_mode.id or
                    registration.event_id.sale_order.payment_mode_id.id or
                    vals.get('payment_mode_id', False))
        return super(AccountInvoice, self).create(vals)
