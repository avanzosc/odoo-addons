# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp


class ProjectProject(models.Model):
    _inherit = 'project.project'

    @api.multi
    @api.depends('user_product_ids', 'user_product_ids.user_id')
    def _compute_members(self):
        for project in self:
            project.members = [
                (6, 0, project.mapped('user_product_ids.user_id').ids)]

    members = fields.Many2many(
        compute='_compute_members', store=True)
    user_product_ids = fields.One2many(
        comodel_name='project.user.product', inverse_name='project_id',
        string='Project users products')


class ProjectTaskWork(models.Model):
    _inherit = "project.task.work"

    @api.model
    def _create_analytic_entries(self, vals):
        task_obj = self.env['project.task']
        timesheet_obj = self.env['hr.analytic.timesheet']
        timeline = super(ProjectTaskWork, self)._create_analytic_entries(vals)
        if (vals.get('task_id', False) and vals.get('user_id', False) and
                vals.get('hours', False)):
            task = task_obj.browse(vals.get('task_id'))
            cond = [('project_id', '=', task.project_id.id),
                    ('user_id', '=', vals.get('user_id'))]
            user_product = self.env['project.user.product'].search(cond,
                                                                   limit=1)
            if user_product:
                time = timesheet_obj.browse(timeline)
                tvals = {'product_id': user_product.product_id.id,
                         'product_uom_id': user_product.product_id.uom_id.id}
                res = time.on_change_unit_amount(
                    user_product.product_id.id, vals.get('hours'), False,
                    False, time.journal_id.id)[0]
                if res and 'amount' in res.get('value', {}):
                    tvals['amount'] = res['value']['amount']
                time.write(tvals)
        return timeline


class ProjectUserProduct(models.Model):
    _name = 'project.user.product'

    project_id = fields.Many2one(
        comodel_name='project.project', string='Project')
    user_id = fields.Many2one(
        comodel_name='res.users', string='User')
    product_id = fields.Many2one(
        comodel_name='product.product', string='Product')
    standard_price = fields.Float(
        string='Cost Price', related='product_id.standard_price',
        digits=dp.get_precision('Product Price'))
    lst_price = fields.Float(
        string='Sale Price', related='product_id.lst_price',
        digits=dp.get_precision('Product Price'))
