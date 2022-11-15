# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    contract_tmpl_line_ids = fields.One2many(
        comodel_name="contract.template.line",
        inverse_name="product_id",
        string="Contract Template Lines",
    )
