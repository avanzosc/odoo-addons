# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestAccountHeadquarter(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountHeadquarter, cls).setUpClass()
        cls.sale_payment_obj = cls.env['sale.advance.payment.inv']
        cls.invoice_obj = cls.env['account.move']
        cls.product_obj = cls.env['product.product']
        cls.sale_order_line_obj = cls.env['sale.order.line']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.resource_calendar = cls.env.ref('resource.resource_calendar_std')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.customer.write({
            'parent_id': cls.company.partner_id.id,
            'headquarter': True})
        cls.product = cls.product_obj.create({
            'name': 'product account headquarter',
            'default_code': 'PACCHEADQUARTER',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'consu',
            'invoice_policy': 'order'})
        cls.product_service = cls.product_obj.create({
            'name': 'product serviceaccount headquarter',
            'default_code': 'PSACCHEADQUARTER',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service',
            'invoice_policy': 'order'})
        sale_vals = {
            "headquarter_id": cls.customer.id,
            "partner_id": cls.customer.id,
            "partner_invoice_id": cls.customer.id,
            "partner_shipping_id": cls.customer.id,
            "company_id": cls.company.id}
        cls.sale = cls.env['sale.order'].create(sale_vals)
        sale_line_vals = {
            'order_id': cls.sale.id,
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        cls.sale_order_line_obj.create(sale_line_vals)
        sale_line_vals = {
            'order_id': cls.sale.id,
            'product_id': cls.product.id,
            'name': cls.product_service.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        cls.sale_order_line_obj.create(sale_line_vals)
        cls.analytic_account = cls.env['account.analytic.account'].search(
            [], limit=1)

    def test_account_headquarter(self):
        self.sale.action_confirm()
        vals = {'advance_payment_method': 'delivered'}
        sale_payment = self.sale_payment_obj.create(vals)
        sale_payment.with_context(active_ids=self.sale.ids).create_invoices()
        cond = [('invoice_origin', '=', self.sale.name)]
        invoice = self.invoice_obj.search(cond, limit=1)
        self.assertEqual(invoice.headquarter_id, self.customer)
        invoice.invoice_line_ids.write(
            {'analytic_account_id': self.analytic_account.id,
             'headquarter_id': invoice.headquarter_id.id})
        invoice.action_post()
        for line in invoice.invoice_line_ids:
            self.assertEqual(len(line.analytic_line_ids), 1)
            for analytic_line in line.analytic_line_ids:
                self.assertEqual(
                    analytic_line.headquarter_id, invoice.headquarter_id)
