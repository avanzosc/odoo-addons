# -*- coding: utf-8 -*-
# © 2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    website_id = fields.Many2one(comodel_name='website.sale', string='Website')

    @api.multi
    def get_plan(self, name):
        instance_obj = self.env['account.analytic.plan.instance']
        plan_obj = self.env['account.analytic.plan']
        analytic_plan = plan_obj.search([])
        if not analytic_plan:
            raise exceptions.Warning(_('You have to create an analytic plan!'))
        plan = instance_obj.search([('name', '=', name)])
        if not plan:
            plan = instance_obj.create({
                'name': name,
                'plan_id': analytic_plan[0].id,
            })
        return plan

    @api.multi
    def get_analytic_account(self, name, parent):
        self.ensure_one()
        analytic_account_obj = self.env['account.analytic.account']
        account = analytic_account_obj.search([('name', '=', name)])
        if not account:
            account = analytic_account_obj.create({'name': name,
                                                   'parent_id': parent.id})
        return account

    @api.multi
    def create_instance_if_necesary(self, account, plan):
        self.ensure_one()
        instance_line_obj = self.env['account.analytic.plan.instance.line']
        line = instance_line_obj.search([
            ('plan_id', '=', plan.id),
            ('analytic_account_id', '=', account.id)])
        if not line:
            instance_line_obj.create({
                'rate': 100.0,
                'analytic_account_id': account.id,
                'plan_id': plan.id,
            })
            return 1
        return 0

    @api.multi
    @api.onchange('product_id', 'website_id')
    def _onchange_website_id(self):
        self.ensure_one()
        res = {}
        parent_id = self.env['res.company'].search([])[0]
        if self.product_id and self.website_id:
            product_name = self.product_id.name
            website_name = self.website_id.name
            plan_name = u'{}-{}'.format(product_name, website_name)
            plan = self.get_plan(plan_name)
            self.analytics_id = plan
            kont = 0
            product_account = self.get_analytic_account(
                product_name, parent_id.parent_product)
            kont += self.create_instance_if_necesary(
                product_account, plan)
            website_account = self.get_analytic_account(
                website_name, parent_id.parent_website)
            kont += self.create_instance_if_necesary(
                website_account, plan)
            if kont >= 2:
                res['warning'] = {
                    'title': _('Warning Message'),
                    'message': _('-- Analytic Distribution --'),
                }
        return res
