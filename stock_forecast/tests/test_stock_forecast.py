# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from openerp import fields
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestStockForecast(common.TransactionCase):

    def setUp(self):
        super(TestStockForecast, self).setUp()
        self.forecast_obj = self.env['product.product.stock.forecast']
        wiz_obj = self.env['stock.immediate.transfer']
        location_obj = self.env['stock.location']
        partner_obj = self.env['res.partner']
        picking_obj = self.env['stock.picking']
        cond = [('code', '=', 'incoming')]
        self.in_picking_type = self.env['stock.picking.type'].search(
            cond, limit=1)
        self.location_supplier = location_obj.search(
            [('usage', '=', 'supplier')], limit=1)
        self.location_customer = location_obj.search(
            [('usage', '=', 'customer')], limit=1)
        cond = [('code', '=', 'outgoing')]
        self.out_picking_type = self.env['stock.picking.type'].search(
            cond, limit=1)
        cond = [('supplier', '=', True)]
        self.supplier = partner_obj.search(cond, limit=1)
        cond = [('customer', '=', True)]
        self.customer = partner_obj.search(cond, limit=1)
        vals = {'name': 'Product for TestProductProductStockForecast',
                'type': 'product'}
        self.product = self.env['product.product'].create(vals)
        picking_vals = {
            'partner_id': self.supplier.id,
            'picking_type_id': self.in_picking_type.id,
            'location_id': self.location_supplier.id,
            'location_dest_id':
            self.in_picking_type.default_location_dest_id.id}
        picking_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 20,
            'product_uom': self.product.uom_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        self.picking = picking_obj.create(picking_vals)
        self.picking.action_confirm()
        wizard_vals = {'pick_ids': [(6, 0, self.picking.ids)]}
        wizard = wiz_obj.create(wizard_vals)
        wizard.process()
        date_expected = (fields.Datetime.from_string(
            self.picking.move_lines[0].date_expected) - relativedelta(years=1))
        date_expected_without_hour = (fields.Datetime.from_string(
            self.picking.move_lines[0].date_expected_without_hour) -
            relativedelta(years=1))
        self.picking.move_lines[0].write(
            {'date_expected': date_expected,
             'date_expected_without_hour': date_expected_without_hour})
        self.picking2 = self.picking.copy()
        self.picking2.move_lines[0].product_uom_qty = 5
        self.picking2.action_confirm()
        wizard_vals = {'pick_ids': [(6, 0, self.picking2.ids)]}
        wizard = wiz_obj.create(wizard_vals)
        wizard.process()
        date_expected = (fields.Datetime.from_string(
            self.picking2.move_lines[0].date_expected) +
            relativedelta(years=1))
        date_expected_without_hour = (fields.Datetime.from_string(
            self.picking2.move_lines[0].date_expected_without_hour) +
            relativedelta(years=1))
        self.picking2.move_lines[0].write(
            {'date_expected': date_expected,
             'date_expected_without_hour': date_expected_without_hour})
        picking_vals = {
            'partner_id': self.customer.id,
            'picking_type_id': self.out_picking_type.id,
            'location_id': self.out_picking_type.default_location_src_id.id,
            'location_dest_id': self.location_customer.id}
        picking_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 2,
            'product_uom': self.product.uom_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        self.out_picking = picking_obj.create(picking_vals)
        self.out_picking.action_confirm()
        self.out_picking.move_lines[0].write(
            {'date_expected': self.picking2.move_lines[0].date_expected,
             'date_expected_without_hour':
             self.picking2.move_lines[0].date_expected_without_hour})

    def test_stock_forecast_from_template(self):
        t = self.product.product_tmpl_id
        t.action_view_product_stock_forecast_from_template()
        cond = [('product_id', '=', self.product.id)]
        forecasts = self.forecast_obj.search(cond)
        forecast = forecasts.filtered(
            lambda c: c.qty_available != 0 or c.incoming_qty != 0 or
            c.outgoing_qty != 0 or c.virtual_available != 0)
        self.assertEqual(forecast.qty_available, 25.0)
        self.assertEqual(forecast.incoming_qty, 0.0)
        self.assertEqual(forecast.outgoing_qty, 2.0)
        self.assertEqual(forecast.virtual_available, 23.0)

    def test_forecast_from_product(self):
        self.product.action_view_product_stock_forecast_from_product()
        cond = [('product_id', '=', self.product.id)]
        forecasts = self.forecast_obj.search(cond)
        forecast = forecasts.filtered(
            lambda c: c.qty_available != 0 or c.incoming_qty != 0 or
            c.outgoing_qty != 0 or c.virtual_available != 0)
        self.assertEqual(forecast.qty_available, 25.0)
        self.assertEqual(forecast.incoming_qty, 0.0)
        self.assertEqual(forecast.outgoing_qty, 2.0)
        self.assertEqual(forecast.virtual_available, 23.0)

    def test_stock_forecast_from_sale_order(self):
        sale_vals = {
            'partner_id': self.customer.id}
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom': self.product.uom_id.id,
            'price_unit': 25.0}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        sale = self.env['sale.order'].create(sale_vals)
        sale.action_view_products_stock_forecast_from_sale()
        cond = [('product_id', '=', self.product.id)]
        forecasts = self.forecast_obj.search(cond)
        forecast = forecasts.filtered(
            lambda c: c.qty_available != 0 or c.incoming_qty != 0 or
            c.outgoing_qty != 0 or c.virtual_available != 0)
        self.assertEqual(forecast.qty_available, 25.0)
        self.assertEqual(forecast.incoming_qty, 0.0)
        self.assertEqual(forecast.outgoing_qty, 2.0)
        self.assertEqual(forecast.virtual_available, 23.0)
