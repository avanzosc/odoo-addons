
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_fsc_certificate = fields.Boolean('Is FSC certificate')

    def fsc_update_orders(self):
        for record in self:
            if record.product_variant_id:
                record.product_variant_id.onchange_fsc_update_orders()
            for product in record.product_variant_ids:
                product.onchange_fsc_update_orders()


class ProductProduct(models.Model):
    _inherit = "product.product"

    is_fsc_certificate = fields.Boolean('Is FSC certificate', related="product_tmpl_id.is_fsc_certificate")

    def onchange_fsc_update_orders(self):
        for record in self:
            order_lines = self.env['sale.order.line'].search([
                ('product_id', '=', record.id)
            ])
            orders = order_lines.mapped('order_id')
            orders.recalc_fsc_certificated()
