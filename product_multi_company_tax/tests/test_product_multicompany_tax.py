# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestProductMultiCompanyTax(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestProductMultiCompanyTax, cls).setUpClass()
        cls.product_obj = cls.env['product.product']
        cls.company_obj = cls.env['res.company']
        cls.tax_obj = cls.env['account.tax']
        partner_vals = {
            'name': 'My partner for test',
            'company_type': 'company'}
        cls.partner = cls.env['res.partner'].create(partner_vals)
        company_vals = {
            'name': 'My company for test',
            'partner_id': cls.partner.id}
        cls.company = cls.env['res.company'].create(company_vals)
        tax_values = {
            'type_tax_use': 'sale',
            'account_id': cls.env.ref(
                'l10n_es.account_common_477').id,
            'name': 'IVA 21% (Bienes), new company',
            'refund_account_id': cls.env.ref(
                'l10n_es.account_common_477').id,
            'chart_template_id': cls.env.ref(
                'l10n_es.account_chart_template_common').id,
            'amount': 21,
            'amount_type': 'percent'}
        cls.tax_customer = cls.tax_obj.create(tax_values)
        tax_values = {
            'type_tax_use': 'purchase',
            'account_id': cls.env.ref(
                'l10n_es.account_common_472').id,
            'name': '21% IVA soportado (bienes corrientes), new company',
            'refund_account_id': cls.env.ref(
                'l10n_es.account_common_472').id,
            'chart_template_id': cls.env.ref(
                'l10n_es.account_chart_template_common').id,
            'amount': 21,
            'amount_type': 'percent'}
        cls.tax_supplier = cls.tax_obj.create(tax_values)
        company_vals = {
            'account_sale_tax_id': cls.tax_customer.id,
            'account_purchase_tax_id': cls.tax_supplier.id}
        cls.company.write(company_vals)
        cls.product = cls.env.ref('product.product_product_7')
        product_vals = {
            'taxes_id': [(6, 0, [cls.tax_customer.id])],
            'supplier_taxes_id': [(6, 0, [cls.tax_supplier.id])],
            'company_ids': [(6, 0, [cls.env.user.company_id.id,
                                    cls.company.id])]}
        cls.product.write(product_vals)

    def test_product_multic_company_tax(self):
        self.product_obj.product_put_tax_multicompany()
        select = ('SELECT COUNT(*) FROM product_taxes_rel '
                  'WHERE prod_id = {}').format(self.product.id)
        self.env.cr.execute(select)
        found = self.env.cr.fetchone()[0]
        self.assertEqual(found, 2)
        select = ('SELECT COUNT(*) FROM product_supplier_taxes_rel '
                  'WHERE prod_id = {}').format(self.product.id)
        self.env.cr.execute(select)
        found = self.env.cr.fetchone()[0]
        self.assertEqual(found, 2)
