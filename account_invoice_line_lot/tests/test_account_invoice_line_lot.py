# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestAccountInvoiceLineLot(TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceLineLot, self).setUp()
        cond = [('state', '=', 'draft')]
        self.sale = self.env['sale.order'].search(cond, limit=1)
        self.wiz_obj = self.env['sale.advance.payment.inv']
        self.sale.action_confirm()
        for move in self.sale.picking_ids[0].move_lines:
            move.write({'quantity_done': move.product_uom_qty})
        self.sale.picking_ids[0].button_validate()
        for move in self.sale.picking_ids[0].move_line_ids:
            vals = {'product_id': move.product_id.id,
                    'product_qty': move.product_qty}
            self.lot = self.env['stock.production.lot'].create(vals)
            move.lot_id = self.lot.id

    def test_account_invoice_line_lot(self):
        wiz = self.wiz_obj.create({'advance_payment_method': 'delivered'})
        wiz.with_context(
            active_ids=[self.sale.id]).create_invoices()
        invoice_line = self.sale.invoice_ids[0].invoice_line_ids[0]
        self.assertEqual(invoice_line.lot_ids, self.lot)
