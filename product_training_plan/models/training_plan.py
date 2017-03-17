# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class TrainingPlan(models.Model):
    _name = 'training.plan'
    _despcription = 'Training plan'

    name = fields.Char(string="Description")
    category_id = fields.Many2one(
        comodel_name='product.category', string='Category')
    planification = fields.Text(string="Planification")
    resolution = fields.Text(string="Resolution")
    html_info = fields.Html(string='Description', translate=True)
    url = fields.Char(string='URL')
