# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestFleetRouteSupportCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteSupportCommon, cls).setUpClass()
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
        cls.passenger = cls.env["res.partner"].create({
            "name": "Passenger",
            "educational_category": "student",
        })
        cls.route = cls.env["fleet.route"].create({
            "name": "Route for test fleet_route",
            "manager_id": cls.employee.id,
            "vehicle_id": cls.vehicle.id,
            "stop_ids": [(0, 0, {
                "name": "Route Stop",
                "location_id": cls.location.id,
            })],
        })
        cls.stop = cls.env["fleet.route.stop"].create({
            "name": "Route Stop 1",
            "route_id": cls.route.id,
            "passenger_ids": [(0, 0, {
                "partner_id": cls.passenger.id,
            })]
        })
        cls.support_model = cls.env["fleet.route.support"]
        cls.support_vals = {
            "student_id": cls.passenger.id,
            "type": "note",
        }
