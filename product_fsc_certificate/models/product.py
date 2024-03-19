from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_fsc_certificate = fields.Boolean(
        string="Is FSC certificate",
    )
