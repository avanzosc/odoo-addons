# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class TrainingPlanCategory(models.Model):
    _name = 'training.plan.category'
    _despcription = 'Training plan category'

    name = fields.Char(string="Description")


class TrainingPlan(models.Model):
    _name = 'training.plan'
    _despcription = 'Training plan'

    @api.multi
    def _get_default_category_id(self):
        try:
            id = self.env.ref(
                'product_training_plan.training_plan_category1').id
        except:
            id = False
        return id

    name = fields.Char(string="Description")
    category_id = fields.Many2one(
        comodel_name='training.plan.category', string='Category',
        default=_get_default_category_id)
    tag_ids = fields.Many2many(
        comodel_name='training.plan.category', string='Tags')
    planification = fields.Text(string="Planification")
    resolution = fields.Text(string="Resolution")
    html_info = fields.Html(string='Description', translate=True)
    url = fields.Char(string='URL')
