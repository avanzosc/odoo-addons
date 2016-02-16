# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestPurchaseOrderLineWithSaleAccount(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseOrderLineWithSaleAccount, self).setUp()
        self.procurement_model = self.env['procurement.order']
        self.sale_model = self.env['sale.order']
        product = self.env.ref('product.product_product_36')
        product.categ_id.procured_purchase_grouping = 'line'
        product.route_ids = [(6, 0,
                              [self.ref('purchase.route_warehouse0_buy'),
                               self.ref('stock.route_warehouse0_mto')])]
        account_vals = {'name': 'purchase_order_line_with_sale_account',
                        'date_start': '2016-01-15',
                        'date': '2016-02-28'}
        self.account = self.env['account.analytic.account'].create(
            account_vals)
        sale_vals = {
            'partner_id': self.ref('base.res_partner_1'),
            'partner_shipping_id': self.ref('base.res_partner_1'),
            'partner_invoice_id': self.ref('base.res_partner_1'),
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id': self.account.id}
        sale_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'product_uom_qty': 7,
            'product_uos_qty': 7,
            'product_uom': product.uom_id.id,
            'price_unit': product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)

    def test_sale_order_create_event(self):
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
            proc.purchase_line_id.account_analytic_id, False,
            'Purchase line without analytic account')
