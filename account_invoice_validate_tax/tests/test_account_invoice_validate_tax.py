# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo.exceptions import ValidationError


@common.at_install(False)
@common.post_install(True)
class TestAccountInvoiceValidateTax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceValidateTax, cls).setUpClass()
        cls.account = cls.env['account.account'].search([], limit=1)
        cls.tax = cls.env['account.tax'].search([], limit=1)
        cls.partner = cls.env['res.partner'].search([], limit=1)
        cls.product = cls.env.ref('product.product_product_3')
        invoice_vals = {'name': 'For test account_invoice_validate_tax',
                        'partner_id': cls.partner.id,
                        'type': 'out_invoice',
                        'currency_id': cls.env.ref("base.ARS").id}
        line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'account_id': cls.account.id,
            'quantity': 1,
            'price_unit': 800}
        invoice_vals['invoice_line_ids'] = [(0, 0, line_vals)]
        cls.invoice = cls.env['account.invoice'].create(invoice_vals)

    def test_account_invoice_validate_tax(self):
        with self.assertRaises(ValidationError):
            self.invoice.action_invoice_open()
        self.invoice.invoice_line_ids.write(
            {'invoice_line_tax_ids': [(6, 0, self.tax.ids)]})
        self.invoice.action_invoice_open()
        self.assertEquals(self.invoice.state, 'open')
