# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class ProductBrand(models.Model):
    _inherit = "product.brand"

    sequence = fields.Integer(string="Sequence")
