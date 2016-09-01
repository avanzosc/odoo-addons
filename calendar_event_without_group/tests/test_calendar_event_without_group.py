# -*- coding: utf-8 -*-
# © 2016 Alfredo de la Fuente - AvanzOSC
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common
from openerp import exceptions


class TestCalendarEventWithoutGroup(common.TransactionCase):

    def setUp(self):
        super(TestCalendarEventWithoutGroup, self).setUp()
        self.calendar_event_model = self.env['calendar.event']
        self.calendar = self.env.ref('calendar.calendar_event_7')
        self.user_demo = self.ref('base.user_demo')

    def test_sale_order_create_event_by_task(self):
        with self.assertRaises(exceptions.Warning):
            self.calendar.sudo(self.user_demo).write({'description': 'a'})
