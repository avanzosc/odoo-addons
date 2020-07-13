# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.fleet_route.tests.common import TestFleetRouteCommon


class TestFleetRouteSchoolCommon(TestFleetRouteCommon):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteSchoolCommon, cls).setUpClass()
        cls.route = cls.route_model.create(cls.route_vals)
        cls.passenger = cls.env["res.partner"].create({
            "name": "Passenger",
            "educational_category": "student",
            "bus_passenger": "yes",
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
            })]
        })
        cls.stop2 = cls.stop_model.create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
            })]
        })
        cls.stop3 = cls.stop_model.create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
            })]
        })
