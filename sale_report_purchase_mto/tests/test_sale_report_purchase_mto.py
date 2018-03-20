# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests import common


class TestSaleReportPurchaseMTO(common.TransactionCase):

    def setUp(self):
        super(TestSaleReportPurchaseMTO, self).setUp()
        self.product_model = self.env['product.product']
        self.sale_model = self.env['sale.order']
        self.sale_report_mto_model = self.env['report.sale.purchase.mto']
        self.procurement_model = self.env['procurement.order']
        self.supplier = self.env.ref('base.res_partner_5')
        product_vals = {
            'name': 'Test MTO product',
            'default_code': 'TEST',
            'type': 'product',
            'standard_price': 5,
            'list_price': 25,
            'route_ids': [(6, 0, [self.ref('purchase.route_warehouse0_buy'),
                                  self.ref('stock.route_warehouse0_mto')])],
            'seller_ids': [(0, 0, {'name': self.supplier.id})]
        }
        self.product = self.product_model.create(product_vals)
        sale_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_uom_qty': 15,
            'product_uos_qty': 15,
            'product_uom': self.product.uom_id.id,
            'price_unit': self.product.list_price
        }
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.ref('product.list0'),
            'order_line': [(0, 0, sale_line_vals)],
            'order_policy': 'picking',
            }
        self.sale_order = self.sale_model.create(sale_vals)
        self.sale_order.action_button_confirm()

    def test_sale_report_mto(self):
        report_lines = self.sale_report_mto_model.search(
            [('sale_id', '=', self.sale_order.id)])
        self.assertFalse(report_lines)
        procurements = self.procurement_model.search(
            [('group_id', '=', self.sale_order.procurement_group_id.id)])
        procurements.run()
        report_lines = self.sale_report_mto_model.search(
            [('sale_id', '=', self.sale_order.id)])
        self.assertEqual(len(report_lines), 1)
        for picking in self.sale_order.picking_ids:
            picking.force_assign()
            picking.action_done()
        report_lines = self.sale_report_mto_model.search(
            [('sale_id', '=', self.sale_order.id)])
        self.assertFalse(report_lines)
