# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestFleetRouteSupportCommon
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRouteSupport(TestFleetRouteSupportCommon):

    def test_fleet_route_support(self):
        self.assertEquals(len(self.passenger.bus_issue_ids), 1)
        support = self.support_model.create({
            "student_id": self.passenger.id,
            "type": "note",
        })
        self.assertEquals(self.passenger, support.student_id)
        self.assertTrue(self.passenger.bus_issue_ids)
        self.assertEquals(
            self.passenger.bus_issue_count, len(self.passenger.bus_issue_ids))
        action_dict = self.passenger.button_bus_issues()
        self.assertTrue('default_student_id' in action_dict['context'])
        self.assertEquals(
            self.passenger.id,
            action_dict['context'].get('default_student_id'))
        self.assertIn(
            ('student_id', 'in', self.passenger.ids),
            action_dict['domain'])
        stop_ids = self.route_support._getPassengerStopDomain()[
            'domain']['low_stop_id'][0][2]
        self.assertEquals(len(stop_ids), 3)
