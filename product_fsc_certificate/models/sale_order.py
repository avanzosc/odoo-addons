
from odoo import api, fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    is_fsc_certificate = fields.Boolean(
        string="FSC certificate",
        related="product_id.is_fsc_certificate",
    )


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_fsc_certificate = fields.Boolean(
        string="Contains FSC certificate",
        compute="_compute_contains_fsc_products",
        store=True,
    )

    @api.depends(
        "order_line", "order_line.product_id",
        "order_line.product_id.is_fsc_certificate")
    def _compute_contains_fsc_products(self):
        for record in self:
            record.is_fsc_certificate = any(
                record.mapped("order_line.product_id.is_fsc_certificate"))

