# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from datetime import datetime


class TestSaleOrderOfferVersion(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestSaleOrderOfferVersion, cls).setUpClass()
        cond = [('is_offer_type', '=', True)]
        cls.offer_type = cls.env["sale.order.type"].search(cond, limit=1)
        cls.sale_obj = cls.env['sale.order']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner sale order offer version',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order offer version',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id})
        sale_line_vals = {
            'product_id': cls.product.id,
            'name': cls.product.name,
            'product_uom_qty': 1,
            'product_uom': cls.product.uom_id.id,
            'price_unit': 100}
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id,
            "type_id": cls.offer_type.id,
            "order_line": [(0, 0, sale_line_vals)]}
        cls.sale1 = cls.sale_obj.create(sale_vals)

    def test_sale_order_offer_version(self):
        my_type = self.sale1.with_context(
            default_is_offer_type=True)._default_type_id()
        self.assertEqual(my_type, self.offer_type)
        self.sale1.onchange_type_id()
        self.assertEqual(self.sale1.is_offer_type, True)
        self.sale1.stage = 'pending'
        self.sale1.onchange_stage()
        self.assertEqual(self.sale1.acceptance_date, False)
        self.assertEqual(self.sale1.rejection_date, False)
        self.sale1.stage = 'accepted'
        self.sale1.onchange_stage()
        self.assertEqual(self.sale1.acceptance_date,
                         datetime.now().date())
        self.assertEqual(self.sale1.rejection_date, False)
        self.sale1.stage = 'rejected'
        self.sale1.onchange_stage()
        self.assertEqual(self.sale1.acceptance_date, False)
        self.assertEqual(self.sale1.rejection_date,
                         datetime.now().date())
        self.sale1.action_offer_to_quotation()
        self.assertEqual(self.sale1.count_sale_orders, 1)
        result = self.sale1.action_view_sale_orders()
        domain = result.get('domain')
        my_domain = "[('id', 'in', {})]".format(self.sale1.sale_ids.ids)
        self.assertEqual(str(domain), my_domain)
