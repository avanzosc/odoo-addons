# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.tests import common, tagged
from odoo import fields
from dateutil.relativedelta import relativedelta


@tagged("post_install", "-at_install")
class TestEventPriceShared(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventPriceShared, cls).setUpClass()
        cls.registration_obj = cls.env['event.registration']
        cls.track_obj = cls.env['event.track']
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.student1 = cls.env.ref('base.res_partner_18')
        cls.student2 = cls.env.ref('base.res_partner_10')
        cls.resource_calendar = cls.env.ref('resource.resource_calendar_std')
        cls.amounced_stage = cls.env.ref('event.event_stage_announced')
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        vals = {'name': 'User event price shared',
                'login': 'ueps@avanzosc.es'}
        cls.user = cls.env['res.users'].create(vals)
        vals = {'name': 'employee event price shared',
                'user_id': cls.user.id}
        cls.env['hr.employee'].create(vals)
        cls.product = cls.env['product.product'].create({
            'name': 'product event price sahred',
            'default_code': 'PEPS',
            'uom_id': cls.uom_unit.id,
            'uom_po_id': cls.uom_unit.id,
            'type': 'service',
            'service_tracking': 'task_in_project',
            'invoice_policy': 'order',
            'service_policy': 'delivered_timesheet',
            'event_ok': True})
        cls.event = cls.env['event.event'].create({
            'name': 'Event event_price_shared',
            'date_begin': fields.Date.today(),
            'date_end': fields.Date.today() + relativedelta(days=+7),
            'shared_price_event': True,
            'organizer_id': cls.customer.id,
            'customer_id': cls.customer.id,
            'resource_calendar_id': cls.resource_calendar.id,
            'main_responsible_id': cls.user.id,
            'event_ticket_ids': [(0, 0, {'product_id': cls.product.id,
                                         'name': cls.product.name,
                                         'price': 50})]
            })

    def test_event_price_shared(self):
        self.event.stage_id = self.amounced_stage.id
        self.assertIsNot(self.event.project_id, False)
        track_vals = {'event_id': self.event.id,
                      'name': 'Session 1',
                      'date': fields.Date.today(),
                      'partner_id': self.user.partner_id.id}
        track = self.track_obj.create(track_vals)
        registration_vals = {
            'event_id': self.event.id,
            'partner_id': self.student1.id,
            'student_id': self.student1.id,
            'event_ticket_id': self.event.event_ticket_ids[0].id,
            'real_date_start': fields.Date.today()}
        registration1 = self.registration_obj.create(registration_vals)
        registration1.action_confirm()
        registration_vals = {
            'event_id': self.event.id,
            'partner_id': self.student2.id,
            'student_id': self.student2.id,
            'event_ticket_id': self.event.event_ticket_ids[0].id,
            'real_date_start': fields.Date.today()}
        registration2 = self.registration_obj.create(registration_vals)
        registration2.action_confirm()
        self.assertEqual(self.event.count_sale_orders, 2)
        sales = self.event.sale_order_lines_ids.mapped('order_id')
        for sale in sales:
            sale.action_confirm()
        self.assertIsNot(registration1.task_id, False)
        self.assertIsNot(registration2.task_id, False)
        self.assertNotEqual(registration1.task_id, registration2.task_id)
        track.button_session_done()
        self.assertEqual(len(track.account_analytic_line_ids), 2)
