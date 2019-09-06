# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, _
from odoo.addons import decimal_precision as dp
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def action_view_product_stock_forecast_from_template(self):
        self.ensure_one()
        self.env['product.product.stock.forecast']._calc_qty_per_day(
            products_lst=self.product_variant_ids)
        action = self.env.ref(
            'stock_forecast.action_product_stock_forecast').read()[0]
        action['domain'] = [('product_id', 'in', self.product_variant_ids.ids)]
        return action


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def action_view_product_stock_forecast_from_product(self):
        self.ensure_one()
        self.env['product.product.stock.forecast']._calc_qty_per_day(
            products_lst=self)
        action = self.env.ref(
            'stock_forecast.action_product_stock_forecast').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action


class ProductProductStockForecast(models.Model):
    _name = 'product.product.stock.forecast'
    _description = 'Product stock forecast'
    _order = 'warehouse_id, date, product_id'

    warehouse_id = fields.Many2one(
        string='Warehouse', comodel_name='stock.warehouse', required=True)
    date = fields.Date(string='date', required=True)
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product', required=True)
    qty_available = fields.Float(
        string='Quantity On Hand',
        digits=dp.get_precision('Product Unit of Measure'))
    virtual_available = fields.Float(
        string='Forecast Quantity',
        digits=dp.get_precision('Product Unit of Measure'))
    incoming_qty = fields.Float(
        string='Incoming', digits=dp.get_precision('Product Unit of Measure'))
    outgoing_qty = fields.Float(
        string='Outgoing', digits=dp.get_precision('Product Unit of Measure'))
    quantities_literal1 = fields.Char(
        string='Quantities literal 1')
    quantities_literal2 = fields.Char(
        string='Quantities literal 2')

    def _calc_qty_per_day(self, products_lst=None):
        warehouses = self.env['stock.warehouse'].search([])
        cond = []
        if products_lst:
            cond.append(('id', 'in', products_lst.ids))
        products = self.env['product.product'].search(cond)
        cond = []
        if products_lst:
            cond.append(('product_id', 'in', products_lst.ids))
        forecast = self.search(cond)
        forecast.unlink()
        moves = self.env['stock.move'].search(cond)
        min_fec = self._catch_min_fec_for_calc_qty_per_day()
        max_fec = self._catch_max_fec_for_calc_qty_per_day(moves)
        if max_fec < min_fec:
            max_fec = min_fec
        while min_fec <= max_fec:
            for warehouse in warehouses:
                for product in products:
                    self._store_qty(warehouse, min_fec, product)
            min_fec = min_fec + relativedelta(days=1)

    def _catch_min_fec_for_calc_qty_per_day(self):
        return fields.Date.context_today(self)

    def _catch_max_fec_for_calc_qty_per_day(self, moves):
        move = max(moves, key=lambda x: x.date_expected_without_hour)
        return move.date_expected_without_hour

    def _store_qty(self, warehouse_id, min_fec, product):
        fec = min_fec + relativedelta(days=1)
        res = product.with_context(
            warehouse=warehouse_id.id)._compute_quantities_dict(
                None, None, None, None, fec)
        literal1 = _('Available: {}, Virtual: {}').format(
            res[product.id]['qty_available'],
            res[product.id]['virtual_available'])
        literal2 = _('Incoming: {}, Outgoing: {}').format(
            res[product.id]['incoming_qty'], res[product.id]['outgoing_qty'])
        vals = {'warehouse_id': warehouse_id.id,
                'date': min_fec,
                'product_id': product.id,
                'qty_available': res[product.id]['qty_available'],
                'incoming_qty': res[product.id]['incoming_qty'],
                'outgoing_qty': res[product.id]['outgoing_qty'],
                'virtual_available': res[product.id]['virtual_available'],
                'quantities_literal1': literal1,
                'quantities_literal2': literal2}
        self.env['product.product.stock.forecast'].create(vals)
