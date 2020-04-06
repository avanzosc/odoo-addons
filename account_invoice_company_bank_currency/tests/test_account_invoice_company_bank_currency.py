# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestAccountInvoiceCompanyBankCurrency(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceCompanyBankCurrency, cls).setUpClass()
        cls.invoice_model = cls.env['account.invoice']

    def test_account_invoice_company_bank_currency(self):
        company = self.env.ref("base.main_company")
        company.partner_id.bank_ids = [
            (0, 0, {'bank_id': self.env.ref("base.bank_bnp").id,
                    'partner_id': company.partner_id.id,
                    'acc_number': 'ACC Number for test',
                    'currency_id': company.currency_id.id,
                    'company_id': company.id})]
        company_bank = company.partner_id.bank_ids.filtered(
            lambda c: c.currency_id)
        self.assertIn(self.invoice_model._get_partner_bank_id(company.id),
                      company_bank)
        company.partner_id.bank_ids[0].currency_id = False
        self.assertIn(self.invoice_model._get_partner_bank_id(company.id),
                      company_bank)
