# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestEventAdditionalMaterial(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventAdditionalMaterial, cls).setUpClass()
        cls.wiz_obj = cls.env['wiz.automatic.material.in.sale.order']
        cls.product = cls.env.ref('product.product_product_4d')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner event additional material',
            'user_id': cls.env.ref('base.user_admin').id})
        sale_vals = {
            "partner_id": cls.partner.id,
            "partner_invoice_id": cls.partner.id,
            "partner_shipping_id": cls.partner.id,
            "company_id": cls.company.id}
        cls.sale = cls.env['sale.order'].create(sale_vals)
        events = cls.env['event.event']. search([])
        for event in events:
            if len(event.registration_ids) > 1:
                cls.event = event
                break
        cls.event.add_mat_automatically = True
        cls.event.registration_ids.action_cancel()
        cls.event.registration_ids.action_set_draft()
        cls.event.registration_ids.write(
            {'sale_order_id': cls.sale.id})
        cls.event.additional_material_ids = [
            (0, 0, {'product_id': cls.product.id,
                    'product_uom_qty': 2,
                    'price_unit': 5})]

    def test_event_registration_action(self):
        self.event.registration_ids.action_confirm()
        number = len(self.event.registration_ids)
        self.assertEqual(
            self.sale.order_line[0].product_uom_qty, number * 2)
        self.assertEqual(
            self.sale.order_line[0].price_unit, 5)
        self.product.lst_price = 88
        self.event.additional_material_ids[0].onchange_product_id()
        self.assertEqual(
            self.event.additional_material_ids[0].price_unit, 88)
        self.sale.order_line[0].unlink()
        self.assertEqual(len(self.sale.order_line), 0)
        wiz = self.wiz_obj.with_context(
            active_model='event.registration',
            active_ids=self.event.registration_ids[0].ids).create({})
        wiz.action_put_material_from_registration()
        self.assertEqual(len(self.sale.order_line), 1)
        self.assertEqual(
            self.sale.order_line[0].product_uom_qty, number * 2)
        self.assertEqual(
            self.sale.order_line[0].price_unit, 88)
