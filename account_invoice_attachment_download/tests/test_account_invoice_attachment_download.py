# -*- coding: utf-8 -*-
# (c) 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from subprocess import Popen, PIPE
import base64


class TestAccountInvoiceAttachmentDownload(common.TransactionCase):

    def setUp(self):
        super(TestAccountInvoiceAttachmentDownload, self).setUp()
        self.invoice_model = self.env['account.invoice']
        self.attachment_model = self.env['ir.attachment']
        self.wiz_model = self.env['wiz.save.invoice.attachment']
        process = Popen(['mktemp',  '-d'], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        file_path = stdout[:-1] + '/' + 'txtfile.txt'
        file = open(file_path, 'w')
        file.write('Line 1\n')
        file.write('Line 2\n')
        file.write('Line 3\n')
        file.close()
        file = open(file_path, 'r')
        datas = base64.encodestring(file.read())
        file.close()
        invoice_vals = {
            'partner_id': self.ref('base.res_partner_2'),
            'type': 'out_invoice',
            'account_id': self.ref('account.fas'),
            'journal_id': self.ref('account.sales_journal')}
        invoice_line_vals = {
            'name': 'product 7',
            'product_id': self.ref('product.product_product_7'),
            'quantity': 5,
            'price_unit': 25
            }
        invoice_vals['invoice_line'] = [(0, 0, invoice_line_vals)]
        self.invoice = self.invoice_model.create(invoice_vals)
        attachment_vals = {
            'res_model': 'account.invoice',
            'datas_fname': 'txtfile.txt',
            'name': 'txtfile.txt',
            'type': 'binary',
            'res_id': self.invoice.id,
            'mimetype': 'text/plain',
            'file_type': 'text/plain',
            'partner_id': self.ref('base.res_partner_2'),
            'index_content': 'aaaaaaaaaaaa',
            'datas': datas,
            'invoice_type': 'out_invoice'}
        self.attachment = self.attachment_model.create(attachment_vals)

    def test_account_invoice_attachment_download(self):
        res = self.wiz_model.with_context(
            active_ids=self.attachment.ids).default_get(['data', 'name'])
        self.assertNotEqual(
            res.get('name'), False, 'No zip file generated')
