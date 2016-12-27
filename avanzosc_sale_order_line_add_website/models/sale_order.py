# -*- coding: utf-8 -*-
# © 2016 AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, exceptions, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    website_id = fields.Many2one(comodel_name='website.sale', string='Website')

    @api.multi
    def _get_plan(self, name):
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
    def _get_analytic_account(self, name, parent):
        analytic_account_obj = self.env['account.analytic.account']
        account = analytic_account_obj.search([('name', '=', name)])
        if not account:
            account = analytic_account_obj.create({'name': name,
                                                   'parent_id': parent.id})
        return account

    @api.multi
    def _create_instance_if_necesary(self, account, plan):
        instance_line_obj = self.env['account.analytic.plan.instance.line']
        line = instance_line_obj.search([
            ('plan_id', '=', plan),
            ('analytic_account_id', '=', account.id)])
        if not line:
            instance_line_obj.create({
                'rate': 100.0,
                'analytic_account_id': account.id,
                'plan_id': plan,
            })
            return 1
        return 0

    @api.multi
    @api.onchange('product_id', 'website_id')
    def _onchange_website_id(self):
        self.ensure_one()
        if self.website_id and self.product_id:
            product_name = self.product_id.name
            website_name = self.website_id.name
            plan = self._update_plan(product_name, website_name)
            self.analytics_id = plan.id

    def _update_plan(self, product_name, website_name):
        plan_name = u'{}-{}'.format(product_name, website_name)
        plan = self._get_plan(plan_name)
        return plan

    @api.multi
    def _create_if_needed_analytic_account_and_instance(
            self, product_name, website_name, plan):
        res = {}
        kont = 0
        parent_id = self.env['res.company'].search([])[0]
        product_account = self._get_analytic_account(
            product_name, parent_id.parent_product)
        kont += self._create_instance_if_necesary(
            product_account, plan)
        website_account = self._get_analytic_account(
            website_name, parent_id.parent_website)
        kont += self._create_instance_if_necesary(
            website_account, plan)
        if kont >= 2:
            res['warning'] = {
                'title': _('Warning Message'),
                'message': _('-- Analytic Distribution --'),
            }
        return res

    @api.model
    def create(self, vals):
        product_obj = self.env['product.product']
        website_obj = self.env['website.sale']
        if 'analytics_id' in vals:
            product_name = product_obj.browse(vals['product_id']).name \
                if vals.get('product_id', False) else self.product_id.name
            website_name = website_obj.browse(vals['website_id']).name \
                if vals.get('website_id', False) else self.website_id.name
            self._create_if_needed_analytic_account_and_instance(
                product_name, website_name, vals['analytics_id'])
        return super(SaleOrderLine, self).create(vals)

    @api.multi
    def write(self, vals):
        product_obj = self.env['product.product']
        website_obj = self.env['website.sale']
        if 'analytics_id' in vals:
            product_name = product_obj.browse(vals['product_id']).name \
                if vals.get('product_id', False) else self.product_id.name
            website_name = website_obj.browse(vals['website_id']).name \
                if vals.get('website_id', False) else self.website_id.name
            self._create_if_needed_analytic_account_and_instance(
                product_name, website_name, vals['analytics_id'])
        return super(SaleOrderLine, self).write(vals)

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False, warehouse_id=False):
        res = super(SaleOrderLine, self).product_id_change_with_wh(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag,
            warehouse_id=warehouse_id)
        if product and self.website_id:
            product_name = self.env['product.product'].browse(product).name
            plan = self._update_plan(product_name, self.website_id.name)
            res['value'].update({'analytics_id': plan.id})
        return res
