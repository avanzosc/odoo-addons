# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.fleet_route_school.tests.common import \
    TestFleetRouteSchoolCommon


class TestFleetRouteSupportCommon(TestFleetRouteSchoolCommon):

    @classmethod
    def setUpClass(cls):
        super(TestFleetRouteSupportCommon, cls).setUpClass()
        cls.support_model = cls.env["fleet.route.support"]
        cls.support_vals = {
            "student_id": cls.passenger.id,
            "type": "note",
        }
