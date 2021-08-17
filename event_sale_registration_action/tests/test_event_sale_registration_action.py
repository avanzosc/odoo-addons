# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestEventSaleRegistationAction(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventSaleRegistationAction, cls).setUpClass()
        cls.confirm_sale_obj = cls.env[
            'wiz.event.registration.confirm.sale.order']
        cls.confirm_participant_sale_obj = cls.env[
            'wiz.event.reg.confirm.participant.sale.order']
        cls.sale_obj = cls.env['sale.order']
        cls.registration_obj = cls.env['event.registration']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.event = cls.env.ref('event.event_0')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Partner event sale registration action',
            'user_id': cls.env.ref('base.user_admin').id})
        cls.product = cls.env['product.product'].create({
            'name': 'Product sale order line contract',
            'default_code': 'Psolc',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id})
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
        cond = [('state', '=', 'draft')]
        cls.registration1 = cls.env['event.registration'].search(cond, limit=1)
        cls.registration1.write(
            {'sale_order_id': cls.sale1.id,
             'sale_order_line_id': cls.sale1.order_line[0].id})
        cls.partner2 = cls.env['res.partner'].create({
            'name': 'Partner event sale registration action',
            'user_id': cls.env.ref('base.user_admin').id})
        sale_vals.update({
            "partner_id": cls.partner2.id,
            "partner_invoice_id": cls.partner2.id,
            "partner_shipping_id": cls.partner2.id})
        cls.sale2 = cls.sale_obj.create(sale_vals)
        cond = [('state', '=', 'draft'),
                ('id', '!=', cls.registration1.id)]
        cls.registration2 = cls.env['event.registration'].search(cond, limit=1)
        cls.registration2.write(
            {'sale_order_id': cls.sale2.id,
             'sale_order_line_id': cls.sale2.order_line[0].id})

    def test_event_sale_registration_action(self):
        wiz = self.confirm_sale_obj.with_context(
            active_model='event.registration',
            active_ids=self.registration1.ids).create({'name': 'a'})
        wiz.action_confirm_sale_order()
        self.assertNotEqual(self.sale1.state, 'draft')
        wiz = self.confirm_participant_sale_obj.with_context(
            active_model='event.registration',
            active_ids=self.registration2.ids).create({'name': 'a'})
        wiz.action_confirm_participant_sale_order()
        self.assertNotEqual(self.sale2.state, 'draft')
        self.assertEqual(self.registration2.state, 'open')
