# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common


class TestStockLotInvoicing(common.TransactionCase):

    def setUp(self):
        super(TestStockLotInvoicing, self).setUp()
        self.picking_model = self.env['stock.picking']
        self.invoice_line_model = self.env['account.invoice.line']
        self.product = self.env.ref('product.product_product_3')
        self.partner = self.ref('base.res_partner_2')
        self.picking_type_out = self.env.ref('stock.picking_type_out')
        self.picking_type_in = self.env.ref('stock.picking_type_in')
        self.in_journal = self.ref('account.expenses_journal')
        self.out_journal = self.ref('account.sales_journal')
        self.lot = self.env['stock.production.lot'].create({
            'name': 'Lot for tests',
            'product_id': self.product.id,
        })
        move_in_vals = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 2.0,
            'restrict_lot_id': self.lot.id,
            'location_id': self.picking_type_in.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_in.default_location_dest_id.id,
        }
        self.picking_in = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': self.picking_type_in.id,
            'invoice_state': '2binvoiced',
            'move_lines': [(0, 0, move_in_vals)],
        })
        move_out_vals = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 2.0,
            'restrict_lot_id': self.lot.id,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_out.default_location_dest_id.id,
        }
        move_out_vals2 = {
            'name': self.product.name,
            'product_id': self.product.id,
            'product_uom': self.product.uom_id.id,
            'product_uom_qty': 2.0,
            'location_id': self.picking_type_out.default_location_src_id.id,
            'location_dest_id':
                self.picking_type_out.default_location_dest_id.id,
        }
        self.picking_out = self.picking_model.create({
            'partner_id': self.partner,
            'picking_type_id': self.picking_type_out.id,
            'invoice_state': '2binvoiced',
            'move_lines': [(0, 0, move_out_vals), (0, 0, move_out_vals2)],
        })
        self.picking_in.action_confirm()
        self.picking_in.action_assign()
        self.picking_in.do_transfer()
        self.picking_out.action_confirm()
        self.picking_out.action_assign()

    def test_onchange_lot_prices(self):
        self.lot.percentage = 30
        self.lot.unit_price = 150
        self.lot.onchange_unit_price_percentage()
        self.assertEqual(self.lot.cost_price, (150 * 30 / 100),
                         'Wrong lot cost price')

    def test_incoming_invoicing_lots(self):
        self.lot.percentage = 30
        self.lot.unit_price = 150
        self.lot.onchange_unit_price_percentage()
        invoices = self.picking_in.with_context(
            inv_type='in_invoice').action_invoice_create(self.in_journal,
                                                         type='in_invoice')
        lines = self.invoice_line_model.search([('invoice_id', 'in', invoices),
                                                ('lot_id', '=', self.lot.id)])
        self.assertEqual(lines.price_unit, self.lot.cost_price,
                         'Invoice price is not correct')

    def test_outgoing_invoicing_lots(self):
        self.lot.percentage = 30
        self.lot.unit_price = 150
        self.lot.onchange_unit_price_percentage()
        invoices = self.picking_out.with_context(
            inv_type='out_invoice').action_invoice_create(self.out_journal,
                                                          type='out_invoice')
        lines = self.invoice_line_model.search([('invoice_id', 'in', invoices),
                                                ('lot_id', '=', self.lot.id)])
        self.assertEqual(lines.price_unit, self.lot.unit_price,
                         'Invoice price is not correct')
        no_lot_lines = self.invoice_line_model.search(
            [('invoice_id', 'in', invoices), ('lot_id', '=', False)])
        self.assertEqual(no_lot_lines.price_unit, self.product.lst_price,
                         'Invoice price is not correct')
