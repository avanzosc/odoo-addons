# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class AccountAnalyticBillingPlan(models.Model):
    _inherit = 'account.analytic.billing.plan'

    prepayment = fields.Boolean(
        compute='_compute_prepayment', compute_sudo=True, store=True)
    final_invoice = fields.Boolean()
    prepayment_invoice_line_ids = fields.One2many(
        comodel_name='account.invoice.line',
        inverse_name='prepayment_plan_id',
        string='Prepayment Invoice Lines')
    prepayment_amount = fields.Float(
        string='Pending Prepayment Amount', digits=dp.get_precision('Account'),
        compute='_compute_prepayment_amount', store=True)

    @api.depends('product_id', 'product_id.product_tmpl_id',
                 'product_id.product_tmpl_id.property_account_income_id',
                 'product_id.product_tmpl_id.property_account_income_id'
                 '.user_type_id', 'product_id.product_tmpl_id.categ_id.'
                 'property_account_income_categ_id',
                 'product_id.product_tmpl_id.categ_id.'
                 'property_account_income_categ_id.user_type_id')
    def _compute_prepayment(self):
        prepayment_type = self.env.ref('account.data_account_type_prepayments')
        for plan in self:
            accounts = plan.product_id.product_tmpl_id.get_product_accounts()
            plan.prepayment = (
                accounts.get('income').user_type_id == prepayment_type)

    @api.depends('prepayment', 'prepayment_invoice_line_ids',
                 'prepayment_invoice_line_ids.price_subtotal_signed',
                 'prepayment_invoice_line_ids.invoice_id',
                 'prepayment_invoice_line_ids.invoice_id.state')
    def _compute_prepayment_amount(self):
        for plan in self.filtered('prepayment'):
            invoice_lines = plan.prepayment_invoice_line_ids.filtered(
                lambda l: l.invoice_id.state not in ['draft', 'cancel'])
            plan.prepayment_amount = sum(invoice_lines.mapped(
                'price_subtotal_signed'))

    @api.constrains('final_invoice')
    def _check_prepayment_final_invoice(self):
        for plan in self:
            if plan.prepayment and plan.final_invoice:
                raise ValidationError(
                    _('Prepayment line can\'t be final invoice line.'))
            if plan.final_invoice:
                final_invoice_plans = self.search([
                    ('id', '!=', plan.id),
                    ('partner_id', '=', plan.partner_id.id),
                    ('final_invoice', '=', True)])
                if final_invoice_plans.mapped('invoice_id').filtered(
                        lambda i: i.state not in ['cancel']):
                    raise ValidationError(
                        _('You can only check one billing plan as final'
                          ' invoice per partner'))

    @api.multi
    def action_invoice_create(self):
        invoice_obj = self.env['account.invoice']
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}
        if any(self.mapped('final_invoice')) and not len(self) == 1:
            raise _('You can only create a final invoice at a time.')
        for plan in self.filtered(
                lambda p: p.final_invoice and not p.invoice_id and p.amount):
            group_key = (plan.partner_id.id, plan.estimated_billing_date)
            inv_data = plan._prepare_invoice()
            invoice = invoice_obj.create(inv_data)
            references[invoice] = plan
            invoices[group_key] = invoice
            invoices_origin[group_key] = [invoice.origin]
            invoices_name[group_key] = [invoice.name]
            plan.invoice_line_create(invoices[group_key].id, 1.0)
            prepayment_plans = self.search([
                ('partner_id', '=', plan.partner_id.id),
                ('prepayment', '=', True),
                ('prepayment_amount', '!=', 0.0)
            ])
            for prepayment_plan in prepayment_plans:
                prepayment_plan.invoice_line_create(
                    invoices[group_key].id, -1.0)
                if (prepayment_plan.display_name not in invoices_origin[
                        group_key]):
                    invoices_origin[group_key].append(
                        prepayment_plan.display_name)
                if (prepayment_plan.display_name not in invoices_name[
                        group_key]):
                    invoices_name[group_key].append(
                        prepayment_plan.display_name)
            plan.invoice_id = invoices[group_key]
            if references.get(invoices.get(group_key)):
                if plan not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= plan
        for group_key in invoices:
            invoices[group_key].write({
                'name': ', '.join(invoices_name[group_key]),
                'origin': ', '.join(invoices_origin[group_key]),
            })
        for invoice in invoices.values():
            invoice.compute_taxes()
        if self.filtered(lambda p: not p.invoice_id and p.amount):
            return super(AccountAnalyticBillingPlan,
                         self).action_invoice_create()
        if not invoices:
            raise UserError(_('There is no billable plan.'))

    @api.multi
    def _prepare_invoice_line(self, qty):
        """
        Prepare the dict of values to create the new invoice line for a billing
        plan.

        :param qty: float quantity to invoice
        """
        self.ensure_one()
        res = super(AccountAnalyticBillingPlan, self)._prepare_invoice_line(
            qty)
        res.update({
            'prepayment_plan_id': self.id if self.prepayment else False,
        })
        return res
