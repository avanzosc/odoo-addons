
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_fsc_certificate = fields.Boolean('FSC certificate', related="product_id.is_fsc_certificate")


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_fsc_certificate = fields.Boolean(
        'Contains FSC certificate', compute="_compute_contains_fsc_products", store=True)

    def _compute_contains_fsc_products(self):
        for record in self:
            certificates = record.order_line.mapped('product_id').mapped('is_fsc_certificate')
            record.is_fsc_certificate = (True in certificates)

    def recalc_fsc_certificated(self):
        for record in self:
            record._compute_contains_fsc_products()
            record.invoice_ids.recalc_fsc_certificated()
