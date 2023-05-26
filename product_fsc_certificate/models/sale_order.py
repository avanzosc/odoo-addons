
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    fsc_certificate = fields.Boolean('FSC certificate', related="product_id.fsc_certificate")
