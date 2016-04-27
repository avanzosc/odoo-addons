# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from datetime import datetime
from dateutil.relativedelta import relativedelta


class TestPickingInvoicingDate(common.TransactionCase):

    def setUp(self):
        super(TestPickingInvoicingDate, self).setUp()
        self.stock_picking = self.env.ref('stock.incomming_shipment')
        self.partner = self.env.ref('base.res_partner_2')
        self.wiz_obj = self.env['stock.transfer_details']
        self.invoice_wiz = self.env['stock.invoice.onshipping']

    def test_create_invoice(self):
        self.stock_picking.invoice_state = '2binvoiced'
        self.stock_picking.partner_id = self.partner
        self.partner.property_supplier_payment_term = \
            self.partner.property_payment_term
        self.stock_picking.action_confirm()
        res = self.stock_picking.do_enter_transfer_details()
        self.wiz_obj.browse(res.get('res_id')).do_detailed_transfer()
        wizard = self.invoice_wiz.with_context({
            'active_id': self.stock_picking.id,
            'active_ids': [self.stock_picking.id],
        }).create({})
        invoice_ids = wizard.create_invoice()
        invoices = self.env['account.invoice'].browse(invoice_ids)
        self.assertEqual(1, len(invoices))
        self.assertEqual(invoices.type, 'in_invoice')
        payday = self.partner.property_supplier_payment_term.line_ids[0].days
        date = datetime.today() + relativedelta(days=payday)
        date_due = datetime.strftime(date, '%Y-%m-%d')
        self.assertEqual(invoices.date_due, date_due)
