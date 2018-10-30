# -*- coding: utf-8 -*-
# (c) 2018 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import fields


class TestPurchaseDocumentsComments(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseDocumentsComments, self).setUp()
        self.purchase_model = self.env['purchase.order']
        self.picking_model = self.env['stock.picking']
        self.invoice_model = self.env['account.invoice']
        self.product = self.browse_ref('product.product_product_3')
        self.supplier = self.browse_ref('base.res_partner_1')
        self.supplier.write({
            'purchase_comment': 'Purchase comment',
            'purchase_propagated_comment': 'Purchase propagated comment',
            'in_picking_comment': 'In picking comment',
            'in_picking_propagated_comment': 'In picking propagated comment',
            'in_invoice_comment': 'In invoice comment'})

    def test_purchase_order_comment_propagation(self):
        vals = self.purchase_model.onchange_partner_id(self.supplier.id)
        value = vals.get('value')
        self.assertEqual(value.get('comment'), 'Purchase comment')
        self.assertEqual(value.get('propagated_comment'),
                         'Purchase propagated comment')
        purchase_line_vals = {
            'product_id': self.product.id,
            'name': self.product.name,
            'product_qty': 100,
            'price_unit': 5,
            'date_planned': fields.Date.today()}
        purchase_vals = {
            'partner_id': self.supplier.id,
            'pricelist_id': value.get('pricelist_id'),
            'payment_term_id': value.get('payment_term_id'),
            'fiscal_position': value.get('fiscal_position'),
            'location_id': self.ref('stock.stock_location_stock'),
            'state': 'draft',
            'invoice_method': 'order',
            'comment': value.get('comment'),
            'propagated_comment': value.get('propagated_comment'),
            'order_line': [(0, 0, purchase_line_vals)]}
        purchase = self.purchase_model.create(purchase_vals)
        res = purchase._prepare_invoice(purchase, purchase.order_line.ids)
        self.assertEqual(res.get('purchase_comment'),
                         'Purchase propagated comment\nIn invoice comment')
        picking = self.picking_model.browse(purchase.action_picking_create())
        self.assertEqual(picking.purchase_propagated_comment,
                         'In picking propagated comment')
        self.assertIn('Purchase propagated comment',
                      picking.purchase_comment)
        self.assertIn('In picking comment',
                      picking.purchase_comment)

    def test_picking_comment_propagation(self):
        cond = [('origin', '=', 'incoming_shipment main_warehouse')]
        picking = self.picking_model.search(cond, limit=1)
        picking.partner_id = self.supplier.id
        picking.onchange_partner_id()
        self.assertEqual(picking.purchase_propagated_comment,
                         'In picking propagated comment')
        self.assertEqual(picking.purchase_comment, 'In picking comment')
        values = {'partner_id': self.supplier.id,
                  'type': 'in_invoice',
                  'account_id': self.browse_ref('account.a_pay').id}
        invoice = self.invoice_model.browse(
            picking._create_invoice_from_picking(picking, values))
        self.assertIn('In picking propagated comment',
                      invoice.purchase_comment)
        self.assertIn('In invoice comment',
                      invoice.purchase_comment)
        vals = invoice.onchange_partner_id('in_invoice', invoice.partner_id.id)
        value = vals.get('value')
        self.assertEqual(value.get('purchase_comment'), 'In invoice comment')
