# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    catalog_ids = fields.Many2many(
        comodel_name="product.catalog.web",
        relation="catalog_web_product_template_rel",
        column1="product_tmpl_id",
        column2="catalog_id",
        string="Catalogs",
    )
