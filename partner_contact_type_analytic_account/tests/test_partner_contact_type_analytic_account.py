# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestPartnerContactTypeAnalyticAccount(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerContactTypeAnalyticAccount, cls).setUpClass()
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product = cls.env['product.product'].create({
            'name': 'Product partner contact type analytic account',
            'default_code': 'PPCTAA',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service'})
        cls.analytic_account = cls.env['account.analytic.account'].search(
            [], limit=1)
        vals = {
            'name': 'Contact type for contact type analytic account',
            'analytic_account_id': cls.analytic_account.id}
        cls.contact_type = cls.env['res.partner.type'].create(vals)
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.customer.contact_type_id = cls.contact_type.id
        invoice_vals = {
            'partner_id': cls.customer.id,
            'move_type': 'out_invoice',
            'invoice_line_ids': [
                (0, 0, {'product_id': cls.product.id,
                        'name': cls.product.name,
                        'quantity': 1,
                        'price_unit': 5,
                        'product_uom_id': cls.product.uom_id.id,
                        'exclude_from_invoice_tab': False})]}
        cls.invoice = cls.env['account.move'].create(invoice_vals)

    def test_account_headquarter(self):
        self.assertEqual(self.invoice.invoice_line_ids[0].analytic_account_id,
                         self.analytic_account)
