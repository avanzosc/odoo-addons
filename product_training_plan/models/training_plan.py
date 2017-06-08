# -*- coding: utf-8 -*-
# Copyright (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models
from openerp.models import expression


class TrainingPlanCategory(models.Model):
    _name = 'training.plan.category'
    _description = 'Training plan category'

    name = fields.Char(string="Description", required=True, translate=True)


class TrainingPlan(models.Model):
    _name = 'training.plan'
    _description = 'Training plan'
    _order = 'code asc'

    @api.multi
    def _get_default_category_id(self):
        try:
            id = self.env.ref(
                'product_training_plan.training_plan_category1').id
        except Exception:
            id = False
        return id

    name = fields.Char(string='Description', required=True)
    code = fields.Char(string='Code', default='/')
    category_id = fields.Many2one(
        comodel_name='training.plan.category', string='Category',
        default=_get_default_category_id)
    tag_ids = fields.Many2many(
        comodel_name='training.plan.category', string='Tags')
    planification = fields.Text(string='Planification')
    resolution = fields.Text(string='Resolution')
    html_info = fields.Html(string='Description', translate=True)
    url = fields.Char(string='URL')
    product_training_plan_ids = fields.One2many(
        comodel_name='product.training.plan',
        inverse_name='training_plan_id', string='Training plan products')
    other_info_ids = fields.Many2many(
        comodel_name='training.plan.other.info', string='Other info',
        relation='training_plan_other_info_rel', column1='training_plan_id',
        column2='training_other_info_id')
    duration = fields.Float(string='Duration')

    _sql_constraints = [
        ('training_plan_unique_sequence', 'UNIQUE (code)',
         'The training plan code must be unique!'),
    ]

    @api.model
    def create(self, values):
        if values.get('code', '/') == '/':
            values['code'] = self.env['ir.sequence'].next_by_id(
                self.env.ref('product_training_plan.'
                             'training_plan_sequence').id)
        return super(TrainingPlan, self).create(values)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.setdefault('code', self.env['ir.sequence'].next_by_id(
            self.env.ref('product_training_plan.training_plan_sequence').id))
        return super(TrainingPlan, self).copy(default)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        results = super(TrainingPlan, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if not args:
            args = []
        domain = expression.OR([[('name', operator, name)],
                                [('code', operator, name)]])
        domain = expression.AND([domain, args or []])
        more_results = self.search(domain, limit=limit)
        return more_results and more_results.name_get() or results

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name_list = super(TrainingPlan, record).name_get()
            for name in name_list:
                if record.code:
                    new_name = u"{} {}".format(
                        record.code, record.name)
                    name = list(name)
                    name[1] = new_name
                    name = tuple(name)
                res.append(name)
        return res


class TrainingPlanOtherinfo(models.Model):
    _name = 'training.plan.other.info'
    _description = 'Training plan other info'
    _order = 'sequence asc'

    sequence = fields.Integer(string='Sequence')
    training_plan_id = fields.Many2one(
        comodel_name='training.plan', string='Training plan')
