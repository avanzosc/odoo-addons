# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api
import openerp.addons.decimal_precision as dp


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def delivery_set(self):
        super(SaleOrder, self.with_context(
            delivery_cost_info=True)).delivery_set()


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    delivery_standard_price = fields.Float(
        string='Delivery cost price',
        digits_compute=dp.get_precision('Product Price'))

    @api.model
    def create(self, data):
        if (self.env.context.get('delivery_cost_info', False) and
                data.get('is_delivery', False)):
            data['delivery_standard_price'] = (
                self._get_delivery_standard_cost(data.get('order_id')))
        return super(SaleOrderLine, self).create(data)

    def _get_delivery_standard_cost(self, order_id):
        total = 0
        weight = 0
        volume = 0
        quantity = 0
        total_delivery = 0.0
        product_uom_obj = self.env['product.uom']
        sale_obj = self.env['sale.order']
        order = sale_obj.browse(order_id)
        carrier = self.env['delivery.carrier'].browse(order.carrier_id.id)
        grid = self.env['delivery.grid'].browse(
            carrier.grid_get(order.partner_shipping_id.id))
        for line in order.order_line:
            if line.state == 'cancel':
                continue
            if line.is_delivery:
                total_delivery += (
                    line.price_subtotal + sale_obj._amount_line_tax(line))
            if not line.product_id or line.is_delivery:
                continue
            q = product_uom_obj._compute_qty(
                line.product_uom.id, line.product_uom_qty,
                line.product_id.uom_id.id)
            weight += (line.product_id.weight or 0.0) * q
            volume += (line.product_id.volume or 0.0) * q
            quantity += q
        total = (order.amount_total or 0.0) - total_delivery
        return self._get_delivery_standard_cost_from_grid(
            grid, total, weight, volume, quantity)

    def _get_delivery_standard_cost_from_grid(
            self, grid, total, weight, volume, quantity):
        delivery_standard_price = 0.0
        price_dict = {'price': total, 'volume': volume, 'weight': weight,
                      'wv': volume*weight, 'quantity': quantity}
        for line in grid.line_ids:
            test = eval(line.type+line.operator+str(line.max_value),
                        price_dict)
            if test:
                if line.price_type == 'variable':
                    delivery_standard_price = (
                        line.standard_price * price_dict[line.variable_factor])
                else:
                    delivery_standard_price = line.standard_price
                break
        return delivery_standard_price
