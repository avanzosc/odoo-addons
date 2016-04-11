# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestSaleOrderPurchaseSplitInfo(common.TransactionCase):

    def setUp(self):
        super(TestSaleOrderPurchaseSplitInfo, self).setUp()
        self.sale_model = self.env['sale.order']
        self.purchase_model = self.env['purchase.order']
        self.procurement_model = self.env['procurement.order']
        self.wiz_split_model = self.env['wiz.purchase.order.split']
        orderpoint_obj = self.env['stock.warehouse.orderpoint']
        product = self.env.ref('product.product_product_24')
        product.route_ids = [
            (6, 0,
             [self.ref('stock.route_warehouse0_mto'),
              self.ref('purchase.route_warehouse0_buy')])]
        orderpoint_vals = {
            'name': 'Alfredo probe',
            'product_id': product.id,
            'warehouse_id': self.ref('stock.warehouse0'),
            'location_id': self.env.ref('stock.warehouse0').lot_stock_id.id,
            'product_min_qty': 1,
            'product_max_qty': 1,
            'qty_multiple': 1.000,
            'active': True}
        orderpoint_obj.create(orderpoint_vals)
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id}
        sale_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'product_uos_qty': 12,
            'product_uom': product.uom_id.id,
            'price_unit': product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_purchase_split_info(self):
        self.sale_order.action_button_confirm()
        cond = [('sale_line_id', '=', self.sale_order.order_line[0].id)]
        proc = self.procurement_model.search(cond, limit=1)
        cond = [('id', '>', proc.id),
                ('product_uom', '=', proc.product_uom.id),
                ('product_uos_qty', '=', proc.product_uos_qty),
                ('product_qty', '=', proc.product_qty),
                ('product_uos', '=', proc.product_uos.id),
                ('product_id', '=', proc.product_id.id),
                ('group_id', '=', proc.group_id.id)]
        proc = self.procurement_model.search(cond, limit=1)
        if proc.state == 'confirmed':
            proc.run()
        self.assertNotEqual(
            proc.purchase_id, False, 'Procurement without purchase')
        wiz_vals = {'parts': 3,
                    'from_date': '2016-03-30',
                    'each_month': 2}
        wiz = self.wiz_split_model.create(wiz_vals)
        wiz.with_context(
            {'active_ids':
             [proc.purchase_id.id]}).action_split_purchase_order()
        dat = ['each_month', 'only_read', 'from_date', 'parts']
        wiz.with_context(
            {'active_ids': [proc.purchase_id.id]}).default_get(dat)
        self.assertEqual(
            len(proc.purchase_id), 1, 'Purchases no generated')
        wiz.with_context(
            {'active_ids':
             [proc.purchase_id.id]}).action_split_purchase_order()
