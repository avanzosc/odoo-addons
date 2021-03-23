# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    default_packaging_id = fields.Many2one('product.packaging', string='Default Packaging')
