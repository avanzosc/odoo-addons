# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
import time


class TestStockInformationMrpProcurementPlan(common.TransactionCase):

    def setUp(self):
        super(TestStockInformationMrpProcurementPlan, self).setUp()
        self.sale_model = self.env['sale.order']
        self.plan_model = self.env['procurement.plan']
        self.stock_information_model = self.env['stock.information']
        self.wiz_model = self.env['wiz.stock.information']
        vals = {'route_ids':
                [(6, 0,
                  [self.env.ref('stock.route_warehouse0_mto').id,
                   self.env.ref('mrp.route_warehouse0_manufacture').id])]}
        self.env.ref('product.product_product_19').write(vals)
        sale_vals = {
            'partner_id': self.env.ref('base.res_partner_2').id,
            'partner_shipping_id': self.env.ref('base.res_partner_2').id,
            'partner_invoice_id': self.env.ref('base.res_partner_2').id,
            'pricelist_id': self.env.ref('product.list0').id,
            'project_id':
            self.env.ref('project.project_project_1').analytic_account_id.id}
        product = self.env.ref('product.product_product_19')
        sale_line_vals = {
            'product_id': product.id,
            'name': product.name,
            'product_uos_qty': 1,
            'product_uom': product.uom_id.id,
            'price_unit': product.list_price}
        sale_vals['order_line'] = [(0, 0, sale_line_vals)]
        self.sale_order = self.sale_model.create(sale_vals)
        year = time.strftime("%Y")
        self.sale_order.project_id.date_start = str(year) + '-01-01'
        to_date = str(year) + '-12-31'
        self.sale_order.project_id.date = to_date
        wiz_vals = {'company': self.ref('base.main_company'),
                    'to_date': to_date}
        self.wiz = self.wiz_model.create(wiz_vals)

    def test_stock_information_mrp_procurement_plan(self):
        self.sale_order.with_context(show_sale=True).action_button_confirm()
        cond = [('name', 'ilike', self.sale_order.name)]
        plan = self.plan_model.search(cond)
        self.assertNotEqual(
            len(plan), 0, 'It has not generated the PROCUREMENT PLAN,'
                          ' confirming the sales order')
        plan.button_recalculate_stock_info()
        cond = []
        lines = self.stock_information_model.search(cond)
        for line in lines:
            line._compute_week()
            line.show_incoming_procurements_from_plan()
            line.show_outgoing_pending_reserved_moves()
        self.assertNotEqual(
            len(lines), 0, 'It has not generated the STOCK INFORMATION')
        self.wiz.calculate_stock_information()
        cond = []
        informations = self.stock_information_model.search(cond)
        for information in informations:
            information._compute_week()
        informations.write({'first_week': False})
        for information in informations:
            information._compute_week()
        self.assertNotEqual(
            len(informations), 0, 'Stock information no generated')
