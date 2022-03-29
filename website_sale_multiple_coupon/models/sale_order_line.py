from odoo import api, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.model
    def create(self, values):
        product_id = values.get('product_id')
        coupon_program = self.env['coupon.program'].search([
            ('discount_line_product_id', '=', product_id)
        ], limit=1)
        if coupon_program and coupon_program.sequence:
            values.update({
                'sequence': 100 + coupon_program.sequence
            })
        return super(SaleOrderLine, self).create(values)
