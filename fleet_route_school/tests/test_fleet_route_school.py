# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestFleetRouteSchoolCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRouteSchool(TestFleetRouteSchoolCommon):

    def test_fleet_route_school(self):
        self.assertTrue(self.route.stop_ids)
        self.assertEquals(self.stop1.passenger_count, 1)
        self.assertEquals(self.passenger.stop_count, 3)
        for stop in self.passenger.stop_ids:
            self.assertFalse(stop.end_date)
        passengers = self.route.mapped("stop_ids.passenger_ids.partner_id")
        self.assertEquals(self.route.passenger_ids, passengers)
        action_dict = self.passenger.button_open_partner_stops()
        domain = action_dict.get("domain")
        partner_stops = self.passenger_model.search([
            ("partner_id", "=", self.passenger.id)])
        self.assertIn(
            ("id", "in", partner_stops.ids), domain)
        context = action_dict.get("context")
        self.assertEquals(context.get("default_partner_id"), self.passenger.id)
        self.passenger.write({
            "bus_passenger": "no",
        })
        for stop in self.passenger.stop_ids:
            self.assertTrue(stop.end_date)

    def test_possible_products(self):
        for passenger in self.route.mapped("stop_ids.passenger_ids"):
            self.assertIn(
                self.half_product, passenger.possible_route_product_ids)
            self.assertIn(
                self.complete_product, passenger.possible_route_product_ids)

    def test_default_value(self):
        weekday_dict = self.weekday_model.default_get(['dayofweek'])
        attendance_dict = self.calendar_model.default_get(['dayofweek'])
        self.assertEquals(
            weekday_dict.get('dayofweek'), attendance_dict.get('dayofweek'))

    def test_passenger_name_get(self):
        for passenger in self.route.mapped("stop_ids.passenger_ids"):
            self.assertEquals(
                passenger.display_name,
                "{} [{}-{}]".format(
                    passenger.partner_id.display_name,
                    passenger.route_id.name_id.name,
                    passenger.stop_id.name))
