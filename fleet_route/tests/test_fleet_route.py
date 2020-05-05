# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from .common import TestFleetRouteCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRoute(TestFleetRouteCommon):

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
            "[{}] {} ({})".format(
                self.route.route_code, self.route.name_id.name, direction))

    def test_fleet_route_name_search(self):
        route = self.route_model.create(self.route_vals)
        route_search = route._name_search(name=self.route_name.name)
        self.assertIn(route.name_get()[0], route_search)
        all_routes = self.route_model.search([])
        route_search = route._name_search(name="Unknown")
        self.assertEquals(all_routes.name_get(), route_search)

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

    def test_route_stop_location_onchange(self):
        route = self.route_model.create(self.route_vals)
        noname_stop = self.stop_model.new({
            "route_id": route.id,
            "location_id": self.location.id,
        })
        self.assertFalse(noname_stop.name)
        noname_stop._onchange_location_id()
        self.assertEquals(
            noname_stop.name, noname_stop.location_id.display_name)
        name_stop = self.stop_model.new({
            "name": "Stop Name",
            "route_id": route.id,
            "location_id": self.location.id,
        })
        self.assertTrue(name_stop.name)
        name_stop._onchange_location_id()
        self.assertNotEquals(
            name_stop.name, name_stop.location_id.display_name)

    def _get_next_code(self):
        return self.route_sequence.get_next_char(
            self.route_sequence.number_next_actual)
