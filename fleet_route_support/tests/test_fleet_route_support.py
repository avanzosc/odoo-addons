# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from datetime import timedelta
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
        action_dict = self.passenger.button_open_bus_issues()
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
            "date": self.today,
            "student_id": self.passenger.id,
        })
        self.assertEquals(
            low_support.allowed_low_stop_ids,
            self.passenger.mapped("stop_ids.stop_id"))

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
        passenger_stop = self.stop1.passenger_ids.filtered(
            lambda s: s.partner_id == self.passenger)
        self.assertTrue(passenger_stop.check_low_or_change_issue())

    def test_wizard_low_batch(self):
        field_list = self.low_wizard.fields_get_keys()
        self.assertEquals(len(self.passenger.bus_issue_ids), 0)
        low_dict = self.low_wizard.with_context(
            active_ids=self.passenger.ids).default_get(field_list)
        date_end = low_dict.get("date") + timedelta(days=6)
        low_dict.update({
            "date_end": date_end,
            "direction": "coming",
        })
        low = self.low_wizard.create(low_dict)
        self.assertIn(self.passenger, low.partner_ids)
        low.create_low_issues()
        stop1_issues = self.passenger.bus_issue_ids.filtered(
            lambda i: i.low_stop_id == self.stop1)
        stop1_issues_count = len(stop1_issues)
        self.assertEquals(stop1_issues_count, 5)  # No date
        stop2_issues = self.passenger.bus_issue_ids.filtered(
            lambda i: i.low_stop_id == self.stop2)
        stop2_issues_count = len(stop2_issues)
        self.assertEquals(stop2_issues_count, 5)
        stop3_issues = self.passenger.bus_issue_ids.filtered(
            lambda i: i.low_stop_id == self.stop3)
        stop3_issues_count = len(stop3_issues)
        self.assertEquals(stop3_issues_count, 1)
        self.assertEquals(
            len(self.passenger.bus_issue_ids),
            stop1_issues_count + stop2_issues_count + stop3_issues_count)

    def test_wizard_batch(self):
        bus_passenger = self.stop1.passenger_ids.filtered(
            lambda p: p.partner_id == self.passenger)
        field_list = self.batch_wizard.fields_get_keys()
        self.assertEquals(len(self.passenger.bus_issue_ids), 0)
        self.assertFalse(bus_passenger.check_low_or_change_issue())
        stops = self.passenger.stop_ids
        batch_dict = self.batch_wizard.with_context(
            active_ids=stops.ids,
            active_model=stops._name
        ).default_get(field_list)
        batch_dict.update({
            "type": "low",
        })
        batch = self.batch_wizard.create(batch_dict)
        self.assertEquals(
            batch.passenger_ids, self.passenger.stop_ids)
        batch.create_issues()
        self.assertEquals(
            len(self.passenger.bus_issue_ids), len(self.passenger.stop_ids))
        self.assertEquals(
            self.route.get_route_passenger_count(), self.route.passenger_count)
        self.assertEquals(
            len(self.route.route_issue_by_type()),
            len(self.passenger.stop_ids))
        action_dict = self.route.button_open_route_issues()
        self.assertIn(
            ("high_stop_route_id", "=", self.route.id),
            action_dict['domain'])
        self.assertIn(
            ("low_stop_route_id", "=", self.route.id),
            action_dict['domain'])
        self.assertTrue(bus_passenger.check_low_or_change_issue())
