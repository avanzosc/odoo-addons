# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRoute(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRoute, cls).setUpClass()
        cls.user = cls.env["res.users"].create({
            "name": "Test user",
            "login": "test_login",
            "context_map_website_id": cls.env.ref(
                "partner_external_map.google_maps").id,
            "context_route_map_website_id": cls.env.ref(
                "partner_external_map.google_maps").id,
        })
        cls.route_model = cls.env["fleet.route"]
        cls.route_sequence = cls.env.ref("fleet_route.route_code_seq")
        cls.driver1 = cls.env["res.partner"].create({
            "name": "Driver 1",
        })
        cls.driver2 = cls.env["res.partner"].create({
            "name": "Driver 2",
        })
        cls.location = cls.env["res.partner"].create({
            "name": "Route Stop",
            "city": "Madrid",
            "street": "street_test",
            "street2": "street2_test",
            "state_id": cls.env.ref("base.state_es_m").id,
            "country_id": cls.env.ref("base.es").id,
            "category_id": [
                (4, cls.env.ref("fleet_route.stop_location_partner_cat").id)],
        })
        cls.employee = cls.env["hr.employee"].create({
            "name": "Test Employee",
            "work_phone": "11111",
            "mobile_phone": "22222",
        })
        cls.vehicle_model = cls.env["fleet.vehicle.model"].create({
            "name": "Bus",
            "brand_id": cls.env.ref("fleet.brand_volvo").id,
        })
        cls.vehicle = cls.env["fleet.vehicle"].create({
            "model_id": cls.vehicle_model.id,
        })
        cls.route_vals = {
            "name": "Route for test fleet_route",
            "manager_id": cls.employee.id,
            "vehicle_id": cls.vehicle.id,
            "stop_ids": [(0, 0, {
                "name": "Route Stop",
                "location_id": cls.location.id,
            })],
        }

    def test_fleet_route(self):
        code = self._get_next_code()
        self.route = self.route_model.create(self.route_vals)
        self.assertEqual(self.route.manager_phone_mobile, "11111/22222")
        self.assertEqual(
            self.route.manager_id.contact_info, "11111/22222")
        self.assertNotEqual(self.route.route_code, False)
        self.assertEqual(self.route.route_code, code)
        field = self.route._fields['direction']
        direction = field.convert_to_export(self.route.direction, self.route)
        self.assertEqual(
            self.route.display_name,
            "[{}] {} ({})".format(self.route.route_code, self.route.name,
                                  direction))

    def test_fleet_route_one_driver(self):
        self.vehicle.write({
            "driver_id": self.driver1.id,
        })
        route = self.route_model.create(self.route_vals)
        self.assertFalse(route.driver_id)
        route.onchange_vehicle_id()
        self.assertEquals(route.driver_id, self.driver1)

    def test_fleet_route_one_driver_list(self):
        self.vehicle.write({
            "driver_ids": [(4, self.driver2.id)],
        })
        self.assertFalse(self.vehicle.driver_id)
        route = self.route_model.create(self.route_vals)
        self.assertFalse(route.driver_id)
        route.onchange_vehicle_id()
        self.assertEquals(route.driver_id, self.driver2)

    def test_fleet_route_multiple_driver_list(self):
        self.vehicle.write({
            "driver_ids": [(6, 0, [self.driver1.id, self.driver2.id])],
        })
        self.assertFalse(self.vehicle.driver_id)
        route = self.route_model.create(self.route_vals)
        self.assertFalse(route.driver_id)
        route.onchange_vehicle_id()
        self.assertFalse(route.driver_id)

    def test_location_open_map(self):
        route = self.route_model.create(self.route_vals)
        action = route.stop_ids[:1].sudo(self.user.id).open_map()
        self.assertEqual(
            action["url"], "https://www.google.com/maps?ie=UTF8"
                           "&q=street_test street2_test Madrid Madrid Spain")

    def _get_next_code(self):
        return self.route_sequence.get_next_char(
            self.route_sequence.number_next_actual)
