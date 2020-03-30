# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRouteSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteSchool, cls).setUpClass()
        cls.manager = cls.env.ref("base.user_root")
        cls.passenger = cls.env["res.partner"].create({
            "name": "Passenger",
            "educational_category": "student",
        })
        cls.route = cls.env["fleet.route"].create({
            "name": "Test Route",
            "going_manager_id": cls.manager.id,
        })
        cls.stop_model = cls.env["fleet.route.stop"]
        cls.passenger_model = cls.env["fleet.route.stop.passenger"]
        cls.weekday_model = cls.env["fleet.route.stop.weekday"]
        cls.calendar_model = cls.env["resource.calendar.attendance"]
        cls.stop1 = cls.stop_model.create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
                "direction": "round",
            })]
        })
        cls.stop2 = cls.stop_model.create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
                "direction": "going",
            })]
        })
        cls.stop3 = cls.stop_model.create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
                "direction": "coming",
            })]
        })

    def test_fleet_route_school(self):
        self.assertTrue(self.route.stop_ids)
        self.assertEquals(self.stop1.going_passenger_count, 1)
        self.assertEquals(self.stop1.coming_passenger_count, 1)
        self.assertEquals(self.stop2.going_passenger_count, 1)
        self.assertEquals(self.stop2.coming_passenger_count, 0)
        self.assertEquals(self.stop3.going_passenger_count, 0)
        self.assertEquals(self.stop3.coming_passenger_count, 1)
        self.assertEquals(self.passenger.stop_count, 3)
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
                    passenger.partner_id.display_name, passenger.route_id.name,
                    passenger.stop_id.name))
