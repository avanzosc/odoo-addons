# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_product_ids = fields.Many2many(
        string='Sale order products', comodel_name='product.product',
        compute='_compute_sale_product_ids')

    def _compute_sale_product_ids(self):
        for sale in self:
            lines = sale.order_line.filtered(lambda x: x.state != 'cancel')
            if lines:
                products = lines.mapped('product_id')
                sale.sale_product_ids = [(6, 0, products.ids)]

    def action_view_products_stock_forecast_from_sale(self):
        self.ensure_one()
        if self.sale_product_ids:
            self.env['product.product.stock.forecast']. _calc_qty_per_day(
                products_lst=self.sale_product_ids)
            action = self.env.ref(
                'stock_forecast.action_product_stock_forecast_from'
                '_sale').read()[0]
            action['domain'] = [
                ('product_id', 'in', self.sale_product_ids.ids)]
            return action
