# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
import os


class TestPartnerDocumentation(common.TransactionCase):

    def setUp(self):
        super(TestPartnerDocumentation, self).setUp()
        self.doc_tmpl_obj = self.env['partner.document.template']
        self.partner_doc_obj = self.env['partner.document']
        self.attach_obj = self.env['ir.attachment']
        self.partner_obj = self.env['res.partner']
        self.wiz_obj = self.env['wizard.import.partner.document']
        self.partner_customer = self.partner_obj.create(
            {'name': 'Test Customer',
             'customer': True,
             'is_company': True
             })
        self.partner_supplier = self.partner_obj.create(
            {'name': 'Test Supplier',
             'supplier': True,
             'is_company': True
             })
        self.partner_both = self.partner_obj.create(
            {'name': 'Test both',
             'customer': True,
             'supplier': True,
             'is_company': True
             })
        self.path = os.path.abspath(os.path.dirname(__file__))
        self.path1 = u'{}/test_data.csv'.format(self.path)
        self.attachment = self.attach_obj.create({'name': 'Test File',
                                                  'type': 'url',
                                                  'url': self.path1
                                                  })
        self.doc_tmpl_1 = self.doc_tmpl_obj.create(
            {'name': 'Customer document',
             'customer_document': True,
             'payment_req': True,
             'agreement_req': True})
        self.doc_tmpl_2 = self.doc_tmpl_obj.create(
            {'name': 'Supplier document',
             'supplier_document': True,
             'customer_document': False,
             'payment_req': True,
             'site_entry_req': True
             })

    def test_import_partner_documentation(self):
        partner_document_count = self.partner_customer.document_count
        self.assertEqual(partner_document_count, 0,
                         'Error partner document quantity does not match')
        customer_document_tmpls = self.doc_tmpl_obj.search([]).filtered(
            lambda x: x.customer_document is True and
            x.company_id.id == self.env.user.company_id.id or not x.company_id)
        self.wiz_obj.with_context(
            active_id=self.partner_customer.id,
            active_ids=[self.partner_customer.id]).import_partner_document()
        self.assertEqual(len(customer_document_tmpls),
                         len(self.partner_customer.document_lines),
                         'Error partner document quantity does not match')
        self.partner_customer.document_lines[0].write(
            {'document_attachment': self.attachment.id})
        self.assertEqual(self.partner_customer.document_lines[0].
                         document_attachment.id,
                         self.attachment.id, 'Error attachment does not match')

    def test_onchange_documentation_attachment(self):
        self.wiz_obj.with_context(
            active_id=self.partner_customer.id,
            active_ids=[self.partner_customer.id]).import_partner_document()
        self.partner_customer.document_lines[0].\
            document_attachment = self.attachment
        self.partner_customer.document_lines[0].with_context(
            set_partner_id=self.partner_customer.id).\
            _onchange_document_attachment()
        self.assertEqual(self.partner_customer.id,
                         self.attachment.res_id,
                         'Error partner attachment does not match')
        res = self.partner_customer.document_lines[0].show_attachment()
        self.assertEqual(res['res_model'], 'ir.attachment',
                         'Error, view does not match')
        res2 = self.partner_customer.show_attachments()
        self.assertEqual(res2['res_model'], 'ir.attachment',
                         'Error, view does not match')
