# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common


class TestFleetRouteCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteCommon, cls).setUpClass()
        cls.user = cls.env["res.users"].create({
            "name": "Test user",
            "login": "test_login",
            "context_map_website_id": cls.env.ref(
                "partner_external_map.google_maps").id,
            "context_route_map_website_id": cls.env.ref(
                "partner_external_map.google_maps").id,
        })
        cls.route_model = cls.env["fleet.route"]
        cls.stop_model = cls.env["fleet.route.stop"]
        cls.route_sequence = cls.env.ref("fleet_route.route_code_seq")
        cls.driver1 = cls.env["res.partner"].create({
            "name": "Driver 1",
        })
        cls.driver2 = cls.env["res.partner"].create({
            "name": "Driver 2",
        })
        cls.location = cls.env["res.partner"].create({
            "name": "Route Stop Location",
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
        cls.route_name = cls.env["fleet.route.name"].create({
            "name": "Route for test fleet_route",
        })
        cls.route_vals = {
            "name_id": cls.route_name.id,
            "manager_id": cls.employee.id,
            "vehicle_id": cls.vehicle.id,
            "stop_ids": [(0, 0, {
                "name": "Route Stop",
                "location_id": cls.location.id,
            })],
        }
