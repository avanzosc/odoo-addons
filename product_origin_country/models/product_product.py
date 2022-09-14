# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models, fields


class ProductProduct(models.Model):
    _inherit = "product.product"

    origin_id = fields.Many2one(
        string="Origin", comodel_name="res.country")
