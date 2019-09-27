# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRoute(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRoute, cls).setUpClass()
        cls.route_model = cls.env['fleet.route']
        cls.route_sequence = cls.env.ref('fleet_route.route_code_seq')
        cls.employee = cls.env['hr.employee'].create({
            'name': 'Test Employee',
            'work_phone': '11111',
            'mobile_phone': '22222',
        })
        cls.route_vals = {
            'name': 'Route for test fleet_route',
            'manager_id': cls.employee.id,
        }

    def test_fleet_route(self):
        code = self._get_next_code()
        self.route = self.route_model.create(self.route_vals)
        self.assertEqual(self.route.manager_phone_mobile, '11111/22222')
        self.assertEqual(self.route.manager_id.contact_info, '11111/22222')
        self.assertNotEqual(self.route.route_code, False)
        self.assertEqual(self.route.route_code, code)

    def _get_next_code(self):
        return self.route_sequence.get_next_char(
            self.route_sequence.number_next_actual
        )
