# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.fleet_route_school.tests.common import \
    TestFleetRouteSchoolCommon


class TestFleetRouteSupportCommon(TestFleetRouteSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteSupportCommon, cls).setUpClass()
        cls.route_model = cls.env['fleet.route']
        cls.route_name_model = cls.env['fleet.route.name']
        cls.stop_model = cls.env["fleet.route.stop"]
        cls.stop_passenger_model = cls.env["fleet.route.stop.passenger"]
        cls.support_model = cls.env["fleet.route.support"]

        cls.support_vals = {
            "student_id": cls.passenger.id,
            "type": "note",
        }
        cls.route_name = cls.route_name.create({
            'name': 'Fleet route name'
        })
        cls.route = cls.route_model.create({
            'name_id': cls.route_name.id
        })
        cls.stop = cls.stop_model.create({
            'name': 'Fleet route stop',
            'route_id': cls.route.id
        })
        cls.stop_passenger = cls.stop_passenger_model.create({
            'stop_id': cls.stop.id,
            'partner_id': cls.passenger.id,
            'start_date': '2030-09-24'
        })
        cls.route_support = cls.support_model.create({
            'student_id': cls.passenger.id,
            'type': 'low',
            'low_stop_id': cls.stop.id
        })
