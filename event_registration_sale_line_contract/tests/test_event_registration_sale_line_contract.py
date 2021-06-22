# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestEventRegistationSaleLineContract(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventRegistationSaleLineContract, cls).setUpClass()
        cls.sale_obj = cls.env['sale.order']
        cls.registration_obj = cls.env['event.registration']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.event = cls.env.ref('event.event_0')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner sale order line contract',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order line contract',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'recurring_rule_type': 'monthly',
            'recurring_interval': 1})
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100,
            'event_id': cls.event.id}
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)]}
        cls.sale1 = cls.sale_obj.create(sale_vals)

    def test_event_registration_sale_line_contract(self):
        self.sale1._action_confirm()
        self.assertEqual(self.sale1.count_contracts, 1)
        self.assertEqual(len(self.sale1.contract_ids[0].contract_line_ids), 1)
        registration_vals = {
            'event_id': self.event.id,
            'sale_order_line_id': self.sale1.order_line[0].id}
        registration1 = self.registration_obj.create(registration_vals)
        self.assertEqual(registration1.contract_id,
                         self.sale1.contract_ids[0])
