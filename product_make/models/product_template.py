# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    product_make_ids = fields.Many2many(
        string="Makes",
        comodel_name="product.make",
        relation="rel_product_template_make",
        column1="template_id",
        column2="make_id",
    )
