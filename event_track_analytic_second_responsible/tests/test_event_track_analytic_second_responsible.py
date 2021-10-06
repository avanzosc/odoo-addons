# Copyright (c) 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged
from odoo import fields
from dateutil.relativedelta import relativedelta


@tagged("post_install", "-at_install")
class TestEventTrackAnalyticSecondResponsible(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventTrackAnalyticSecondResponsible, cls).setUpClass()
        cls.product_obj = cls.env['product.product']
        cls.sale_order_line_obj = cls.env['sale.order.line']
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.customer = cls.env.ref('base.res_partner_12')
        cls.resource_calendar = cls.env.ref('resource.resource_calendar_std')
        cls.event_confirmed_stage = cls.env.ref('event.event_stage_announced')
        cls.company = cls.env['res.company']._company_default_get('sale.order')
        vals = {'name': 'User event track analytic second responsible',
                'login': 'uetasrt@avanzosc.es'}
        user = cls.env['res.users'].create(vals)
        vals = {'name': 'employee event event track analyticsecondresponsible',
                'user_id': user.id}
        cls.env['hr.employee'].create(vals)
        vals = {'name': 'User2 event track analytic second responsible',
                'login': 'u2etasrt@avanzosc.es'}
        user2 = cls.env['res.users'].create(vals)
        vals = {'name': 'employee2 event track analyticsecondresponsible',
                'user_id': user2.id}
        cls.env['hr.employee'].create(vals)
        cls.event = cls.env['event.event'].create({
            'name': 'Avanzosc Event track analytic second responsible',
            'date_begin': fields.Date.today(),
            'date_end': fields.Date.today() + relativedelta(days=+7),
            'customer_id': cls.customer.id,
            'resource_calendar_id': cls.resource_calendar.id,
            'main_responsible_id': user.id,
            'second_responsible_id': user2.id
            })
        track_vals = {'event_id': cls.event.id,
                      'name': 'Session 1',
                      'date': fields.Date.today(),
                      'partner_id': user.partner_id.id,
                      'second_responsible_id': user2.partner_id.id}
        cls.env['event.track'].create(track_vals)
        cond = [('is_done', '=', True)]
        cls.track_done_state = cls.env['event.track.stage'].search(
            cond, limit=1)

    def test_event_track_analytic_second_reponsible(self):
        self.event.track_ids[0].stage_id = self.track_done_state.id
        self.assertEqual(
            len(self.event.track_ids[0].account_analytic_line_ids), 2)
