# Copyright 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged
from odoo import fields
from dateutil.relativedelta import relativedelta


@tagged("post_install", "-at_install")
class TestEventHeadquarter(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventHeadquarter, cls).setUpClass()
        cls.product_obj = cls.env['product.product']
        cls.sale_order_line_obj = cls.env['sale.order.line']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.resource_calendar = cls.env.ref('resource.resource_calendar_std')
        cls.event_confirmed_stage = cls.env.ref('event.event_stage_announced')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        vals = {'name': 'User event headquarter',
                'login': 'evenheadquartner@avanzosc.es'}
        user = cls.env['res.users'].create(vals)
        user.partner_id.write({'parent_id': cls.company.partner_id.id,
                               'headquarter': True})
        vals = {'name': 'employee event headquarter',
                'user_id': user.id}
        cls.env['hr.employee'].create(vals)
        cls.displacement_product = cls.product_obj.create({
            'name': 'Displacement',
            'default_code': 'DISPLACEMENTJEADQUARTER',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service',
            'service_policy': 'delivered_timesheet',
            'service_tracking': 'task_in_project'})
        cls.product = cls.product_obj.create({
            'name': 'Urban camp',
            'default_code': 'URBANCAMPHEADQUARTER',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service',
            'service_policy': 'delivered_timesheet',
            'service_tracking': 'task_in_project',
            'event_ok': True})
        cls.event = cls.env['event.event'].create({
            'name': 'Avanzosc Event HEADQUARTER',
            'organizer_id': user.partner_id.id,
            'date_begin': fields.Date.today(),
            'date_end': fields.Date.today() + relativedelta(days=+7),
            'customer_id': cls.customer.id,
            'resource_calendar_id': cls.resource_calendar.id,
            'main_responsible_id': user.id,
            'event_ticket_ids': [(0, 0, {'product_id': cls.product.id,
                                         'name': cls.product.name,
                                         'price': 55})]
            })
        track_vals = {'event_id': cls.event.id,
                      'name': 'Session 1',
                      'date': fields.Date.today(),
                      'partner_id': user.partner_id.id}
        cls.env['event.track'].create(track_vals)
        sale_vals = {
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
            'price_unit': 100,
            'event_id': cls.event.id,
            'event_ticket_id': cls.event.event_ticket_ids[0].id}
        cls.sale_order_line_obj.create(sale_line_vals)
        sale_line_vals = {
            'order_id': cls.sale.id,
            'product_id': cls.displacement_product.id,
            'name': cls.displacement_product.name,
            'product_uom_qty': 1,
            'product_uom': cls.displacement_product.uom_id.id,
            'price_unit': 25}
        cls.sale_order_line_obj.create(sale_line_vals)
        cond = [('is_done', '=', True)]
        cls.track_done_state = cls.env['event.track.stage'].search(
            cond, limit=1)

    def test_event_with_displacement(self):
        self.sale.action_confirm()
        self.event.stage_id = self.event_confirmed_stage.id
        self.event.track_ids[0].stage_id = self.track_done_state.id
        self.assertNotEqual(len(self.event.account_analytic_line_ids), 0)
        for line in self.event.account_analytic_line_ids:
            self.assertEqual(line.headquarter_id, self.event.organizer_id)
