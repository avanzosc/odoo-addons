# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import common


class TestInvoiceCustomerRef(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestInvoiceCustomerRef, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.partner_model = cls.env['res.partner']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.sale_model = cls.env['sale.order']
        cls.partner = cls.partner_model.create({
            'name': 'Partner1',
        })
        cls.product = cls.product_model.create({
            'name': 'Product',
            'type': 'product',
            'default_code': 'P1',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id
        })
        cls.sale_order = cls.sale_model.create({
            'partner_id': cls.partner.id,
            'client_order_ref': 'New reference',
            'order_line': [(0, 0, {'product_id': cls.product.id})],
            })

    def test_invoice_ref(self):
        self.sale_order.action_confirm()
        self.sale_order.action_invoice_create()
        self.assertEqual(len(self.sale_order.invoice_ids), 1,
                         "Invoice not created.")
        self.invoice = self.sale_order.invoice_ids
        self.assertEqual(self.invoice.client_order_ref, 'New reference',
                         "Invoice reference do not match.")
        self.invoice.client_order_ref = 'Update Ref Invoice'
        self.assertEqual(self.sale_order.client_order_ref,
                         'Update Ref Invoice',
                         "Sale reference do not match.")
        self.sale_order.client_order_ref = 'Update Ref Sale'
        self.assertEqual(self.invoice.client_order_ref, 'Update Ref Sale',
                         "Invoice reference do not match.")
