# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from .common import TestFleetRouteSupportCommon
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.tests import common


@common.at_install(False)
@common.post_install(True)
class TestFleetRouteSupport(TestFleetRouteSupportCommon):

    def test_fleet_route_support(self):
        self.assertEquals(len(self.passenger.bus_issue_ids), 0)
        support = self.support_model.create({
            "date": fields.Date.today(),
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
        with self.assertRaises(ValidationError):
            self.support_model.create({
                "date": fields.Date.today(),
                "student_id": self.passenger.id,
                "type": "note",
            })

    def test_fleet_route_support_low_stop(self):
        low_support = self.support_model.create({
            "type": "low",
            "date": fields.Date.today(),
            "student_id": self.passenger.id,
        })
        self.assertEquals(
            low_support.allowed_low_stop_ids.ids,
            self.passenger.mapped("stop_ids.stop_id.id"))

    def test_fleet_route_support_high_stop(self):
        high_support = self.support_model.create({
            "type": "high",
            "date": fields.Date.today(),
            "student_id": self.passenger.id,
        })
        self.assertEquals(
            high_support.allowed_high_stop_ids, self.stop_model.search([]))

    def test_fleet_route_support_change_stop(self):
        change_support = self.support_model.create({
            "type": "change",
            "date": fields.Date.today(),
            "student_id": self.passenger.id,
            "low_stop_id": self.stop1.id,
        })
        self.assertEquals(
            change_support.allowed_high_stop_ids, self.stop_model.search([
                ("route_id.direction", "=", self.stop1.route_id.direction),
                ("id", "!=", self.stop1.id),
            ]))

    def test_wizard_low_batch(self):
        field_list = self.low_wizard.fields_get_keys()
        self.assertEquals(len(self.passenger.bus_issue_ids), 0)
        low_dict = self.low_wizard.with_context(
            active_ids=self.passenger.ids).default_get(field_list)
        low_dict.update({
            "direction": "coming",
        })
        low = self.low_wizard.create(low_dict)
        self.assertIn(self.passenger, low.partner_ids)
        low.create_low_issues()
        self.assertEquals(
            len(self.passenger.bus_issue_ids), len(self.passenger.stop_ids))

    def test_wizard_batch(self):
        field_list = self.batch_wizard.fields_get_keys()
        self.assertEquals(len(self.passenger.bus_issue_ids), 0)
        batch_dict = self.batch_wizard.with_context(
            active_ids=self.passenger.stop_ids.ids).default_get(field_list)
        batch_dict.update({
            "type": "low",
        })
        batch = self.batch_wizard.create(batch_dict)
        self.assertEquals(
            batch.passenger_ids, self.passenger.stop_ids)
        batch.create_issues()
        self.assertEquals(
            len(self.passenger.bus_issue_ids), len(self.passenger.stop_ids))
