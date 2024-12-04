# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPackageType(models.Model):
    _inherit = "stock.package.type"

    product_tmpl_id = fields.Many2one(
        string="Product",
        comodel_name="product.template",
        copy=False,
    )
