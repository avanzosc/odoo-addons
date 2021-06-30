# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    plane_number_id = fields.Many2one(
        string='Plane number', comodel_name='product.plane.number')
