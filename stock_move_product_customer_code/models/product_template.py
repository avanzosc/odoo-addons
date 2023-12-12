# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    customer_code_ids = fields.One2many(
        string="Product customer codes",
        comodel_name="product.template.customer.code",
        inverse_name="template_id",
        copy=False,
    )
