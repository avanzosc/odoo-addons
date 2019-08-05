# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestAccountInvoiceUsability(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceUsability, cls).setUpClass()
        invoice_obj = cls.env['account.invoice']
        cls.customer_invoice = invoice_obj.search(
            [('type', '=', 'out_invoice')], limit=1)
        cls.supplier_invoice = invoice_obj.search(
            [('type', '=', 'in_invoice')], limit=1)

    def test_customer_invoice(self):
        self.assertEquals(self.customer_invoice.invoice_line_count,
                          len(self.customer_invoice.invoice_line_ids))
        action_dict = self.customer_invoice.button_open_invoice_lines()
        context = action_dict.get('context')
        self.assertEquals(context.get('default_invoice_id'),
                          self.customer_invoice.id)
        domain = action_dict.get('domain')
        self.assertIn(('invoice_id', '=', self.customer_invoice.id), domain)

    def test_supplier_invoice(self):
        self.assertEquals(self.supplier_invoice.invoice_line_count,
                          len(self.supplier_invoice.invoice_line_ids))
        action_dict = self.supplier_invoice.button_open_invoice_lines()
        context = action_dict.get('context')
        self.assertEquals(context.get('default_invoice_id'),
                          self.supplier_invoice.id)
        domain = action_dict.get('domain')
        self.assertIn(('invoice_id', '=', self.supplier_invoice.id), domain)
