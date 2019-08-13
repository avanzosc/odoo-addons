# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields
from dateutil.relativedelta import relativedelta


class TestStockForecast(common.TransactionCase):

    def setUp(self):
        super(TestStockForecast, self).setUp()
        partner_obj = self.env['res.partner']
        picking_obj = self.env['stock.picking']
        self.report_obj = self.env['report.stock.traceability_operation']
        self.wiz_obj = self.env['stock.transfer_details']
        cond = [('code', '=', 'incoming'),
                ('default_location_src_id', '!=', False),
                ('default_location_dest_id', '!=', False)]
        self.in_picking_type = self.env['stock.picking.type'].search(
            cond, limit=1)
        cond = [('code', '=', 'outgoing'),
                ('default_location_src_id', '!=', False),
                ('default_location_dest_id', '!=', False)]
        self.out_picking_type = self.env['stock.picking.type'].search(
            cond, limit=1)
        cond = [('supplier', '=', True)]
        self.supplier = partner_obj.search(cond, limit=1)
        cond = [('customer', '=', True)]
        self.customer = partner_obj.search(cond, limit=1)
        vals = {'name': 'Product for TestProductProductStockForecast',
                'type': 'product'}
        self.product = self.env['product.product'].create(vals)
        picking_vals = {'partner_id': self.supplier.id,
                        'picking_type_id': self.in_picking_type.id}
        picking_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 20,
            'product_uom': self.product.uom_id.id,
            'location_id': self.in_picking_type.default_location_src_id.id,
            'location_dest_id':
            self.in_picking_type.default_location_dest_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        self.picking = picking_obj.create(picking_vals)
        self.picking.action_confirm()
        res = self.picking.do_enter_transfer_details()
        wizard = self.wiz_obj.browse(res.get('res_id'))
        wizard.do_detailed_transfer()
        date_expected = (fields.Datetime.from_string(
            self.picking.move_lines[0].date_expected) - relativedelta(years=1))
        date_expected_without_hour = (fields.Datetime.from_string(
            self.picking.move_lines[0].date_expected_without_hour) -
            relativedelta(years=1))
        self.picking.move_lines[0].write(
            {'date_expected': date_expected,
             'date_expected_without_hour': date_expected_without_hour})
        in_date = (fields.Datetime.from_string(
            self.picking.move_lines[0].quant_ids[0].in_date) -
            relativedelta(years=1))
        in_date_without_hour = (fields.Datetime.from_string(
            self.picking.move_lines[0].quant_ids[0].in_date_without_hour) -
            relativedelta(years=1))
        self.picking.move_lines[0].quant_ids[0].write(
            {'in_date': in_date,
             'in_date_without_hour': in_date_without_hour})
        self.picking2 = self.picking.copy()
        self.picking2.move_lines[0].product_uom_qty = 5
        self.picking2.action_confirm()
        res = self.picking2.do_enter_transfer_details()
        wizard = self.wiz_obj.browse(res.get('res_id'))
        wizard.do_detailed_transfer()
        date_expected = (fields.Datetime.from_string(
            self.picking2.move_lines[0].date_expected) +
            relativedelta(years=1))
        date_expected_without_hour = (fields.Datetime.from_string(
            self.picking2.move_lines[0].date_expected_without_hour) +
            relativedelta(years=1))
        self.picking2.move_lines[0].write(
            {'date_expected': date_expected,
             'date_expected_without_hour': date_expected_without_hour})
        picking_vals = {'partner_id': self.customer.id,
                        'picking_type_id': self.out_picking_type.id}
        picking_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 2,
            'product_uom': self.product.uom_id.id,
            'location_id': self.out_picking_type.default_location_src_id.id,
            'location_dest_id':
            self.out_picking_type.default_location_dest_id.id}
        picking_vals['move_lines'] = [(0, 0, picking_line_vals)]
        self.out_picking = picking_obj.create(picking_vals)
        self.out_picking.action_confirm()
        self.out_picking.move_lines[0].write(
            {'date_expected': self.picking2.move_lines[0].date_expected,
             'date_expected_without_hour':
             self.picking2.move_lines[0].date_expected_without_hour})

    def test_stock_forecast(self):
        res = self.product.action_traceability_operation()
        lines = self.report_obj.search(res.get('domain'))
        line = min(lines, key=lambda x: x.id)
        self.assertEqual(line.available_qty, 0.0)
        self.assertEqual(line.virtual_available, 0.0)
        self.assertEqual(line.incoming_qty, 0.0)
        self.assertEqual(line.outgoing_qty, 0.0)
        self.assertEqual(line.product_uom_qty, 20.0)
        line = max(lines, key=lambda x: x.id)
        self.assertEqual(line.available_qty, 20.0)
        self.assertEqual(line.virtual_available, 18.0)
        self.assertEqual(line.incoming_qty, 0.0)
        self.assertEqual(line.outgoing_qty, 2.0)
        self.assertEqual(line.product_uom_qty, 5.0)
