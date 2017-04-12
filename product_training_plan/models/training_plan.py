# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class TrainingPlanCategory(models.Model):
    _name = 'training.plan.category'
    _despcription = 'Training plan category'

    name = fields.Char(string="Description", required=True, translate=True)


class TrainingPlan(models.Model):
    _name = 'training.plan'
    _despcription = 'Training plan'
    _order = 'sequence asc'

    @api.multi
    def _get_default_category_id(self):
        try:
            id = self.env.ref(
                'product_training_plan.training_plan_category1').id
        except:
            id = False
        return id

    name = fields.Char(string="Description", required=True)
    sequence = fields.Char(string="Sequence", default="/")
    category_id = fields.Many2one(
        comodel_name='training.plan.category', string='Category',
        default=_get_default_category_id)
    tag_ids = fields.Many2many(
        comodel_name='training.plan.category', string='Tags')
    planification = fields.Text(string="Planification")
    resolution = fields.Text(string="Resolution")
    html_info = fields.Html(string='Description', translate=True)
    url = fields.Char(string='URL')
    product_training_plan_ids = fields.One2many(
        comodel_name='product.training.plan',
        inverse_name='training_plan_id', string='Product training plan')
    other_info_ids = fields.Many2many(
        comodel_name='training.plan.other.info', string='Other info',
        relation='training_plan_other_info_rel', column1='training_plan_id',
        column2='training_other_info_id')
    duration = fields.Float(string='Duration')

    _sql_constraints = [
        ('training_plan_unique_sequence', 'UNIQUE (sequence)',
         'The training plan sequence must be unique!'),
    ]

    @api.model
    def create(self, values):
        if values.get('sequence', '/') == '/':
            values['sequence'] = self.env['ir.sequence'].next_by_id(
                self.env.ref('product_training_plan.'
                             'training_plan_sequence').id)
        return super(TrainingPlan, self).create(values)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        default.setdefault('sequence', self.env['ir.sequence'].next_by_id(
            self.env.ref('product_training_plan.training_plan_sequence').id))
        return super(TrainingPlan, self).copy(default)


class TrainingPlanOtherinfo(models.Model):
    _name = 'training.plan.other.info'
    _despcription = 'Training plan other info'
    _rec_name = 'sequence'

    sequence = fields.Integer(string="Sequence")
    training_plan_id = fields.Many2one(
        comodel_name='training.plan', string='Training plan')
