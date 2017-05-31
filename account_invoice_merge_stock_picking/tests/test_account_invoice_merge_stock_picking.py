# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.stock_picking_invoice_link.tests.\
    test_stock_picking_invoice_link import TestStockPickingInvoiceLink


class TestAccountInvoiceMergeStockPicking(TestStockPickingInvoiceLink):

    def setUp(self):
        super(TestAccountInvoiceMergeStockPicking, self).setUp()
        self.picking_in.invoice_state = '2binvoiced'
        self.picking_in2 = self.picking_in.copy()
        self.picking_in2.invoice_state = '2binvoiced'
        context2 = {"active_model": 'stock.picking',
                    "active_ids": [self.picking_in2.id],
                    "active_id": self.picking_in2.id}
        self.wizard2 = self.env['stock.invoice.onshipping'].with_context(
            context2).create({})

    def test_invoice_merge(self):
        self.wizard.open_invoice()
        invoice = self.picking_in.invoice_id
        self.wizard2.open_invoice()
        invoice2 = self.picking_in2.invoice_id
        invoices = self.env['account.invoice']
        invoices |= invoice
        invoices |= invoice2
        invoices_info, inv_line_info = invoices.do_merge()
        new_invoice_ids = invoices_info.keys()
        self.new_invoice = self.env['account.invoice'].browse(new_invoice_ids)
        self.assertTrue(self.picking_in.id in self.new_invoice.picking_ids.ids)
        self.assertTrue(self.picking_in2.id in
                        self.new_invoice.picking_ids.ids)
        self.assertTrue(self.picking_in.invoice_state == 'invoiced')
        self.assertTrue(self.picking_in2.invoice_state == 'invoiced')
