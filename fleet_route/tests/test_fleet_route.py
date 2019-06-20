# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests.common import TransactionCase


class TestFleetRoute(TransactionCase):

    def setUp(self):
        super(TestFleetRoute, self).setUp()
        self.employee = self.env.ref('hr.employee_fpi')
        self.employee.write({
            'work_phone': '11111',
            'mobile_phone': '22222'})
        route_vals = {
            'name': 'Route for test fleet_route',
            'manager_id': self.employee.id,
            'substitute_id': self.employee.id}
        self.route = self.env['fleet.route'].create(route_vals)

    def test_fleet_route(self):
        self.assertEqual(self.route.manager_phone_mobile, '11111/22222')
        self.assertEqual(self.route.substitute_phone_mobile, '11111/22222')
        self.assertNotEqual(self.route.route_code, False)
