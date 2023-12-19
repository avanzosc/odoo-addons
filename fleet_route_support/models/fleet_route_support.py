# Copyright 2019 Adrian Revilla - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

ISSUE_TYPE = [("high", "High"),
              ("low", "Low"),
              ("change", "Change"),
              ("note", "Note")]
LOW_TYPE = [("lack of assistance", "Lack of assistance"),
            ("pick-up notice", "Pick-up notice")]


class FleetRouteSupport(models.Model):
    _name = "fleet.route.support"
    _description = "Fleet route support"

    date = fields.Date(string="Date", required=True,
                       index=True, copy=False,
                       default=fields.Date.context_today)
    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain="[('educational_category', '=', 'student')]",
        required=True)
    type = fields.Selection(
        selection=ISSUE_TYPE, string="Type",
        required=True)
    allowed_high_stop_ids = fields.Many2many(
        comodel_name="fleet.route.stop", string="Allowed High Stops",
        compute="_compute_allowed_high_stop_ids")
    high_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="High stop")
    high_stop_route_id = fields.Many2one(
        related="high_stop_id.route_id", comodel_name="fleet.route",
        string="High stop route", store=True)
    high_stop_direction = fields.Selection(
        related="high_stop_id.route_id.direction",
        string="High stop direction")
    allowed_low_stop_ids = fields.Many2many(
        comodel_name="fleet.route.stop", string="Allowed Low Stops",
        compute="_compute_allowed_low_stop_ids")
    low_stop_id = fields.Many2one(
        comodel_name="fleet.route.stop", string="Low stop")
    low_stop_route_id = fields.Many2one(
        related="low_stop_id.route_id", comodel_name="fleet.route",
        string="Low stop route", store=True)
    low_stop_direction = fields.Selection(
        related="low_stop_id.route_id.direction", string="Low stop direction")
    notes = fields.Text(string="Incidence description")
    low_type = fields.Selection(
        selection=LOW_TYPE, string="Low type")

    @api.constrains(
        "date", "student_id", "type", "low_stop_id", "high_stop_id")
    def _check_duplicity(self):
        issue_obj = self.env["fleet.route.support"]
        for record in self:
            domain = [
                ("date", "=", record.date),
                ("student_id", "=", record.student_id.id),
                ("type", "=", record.type),
                ("id", "!=", record.id),
            ]
            if record.type in ("low", "change"):
                domain.append(("low_stop_id", "=", record.low_stop_id.id))
            elif record.type in ("high"):
                domain.append(("high_stop_id", "=", record.high_stop_id.id))
            other_issues = issue_obj.search(domain)
            if other_issues:
                raise ValidationError(
                    _("There must only be one issue per day, type and"
                      " student!"))

    @api.multi
    @api.depends("date", "type", "student_id", "student_id.stop_ids",
                 "student_id.stop_ids.start_date",
                 "student_id.stop_ids.end_date")
    def _compute_allowed_low_stop_ids(self):
        for record in self.filtered(lambda r: r.type in ("low", "change")):
            record.allowed_low_stop_ids = (
                record.student_id.stop_ids.filtered(
                    lambda s:
                    ((s.start_date and (s.start_date <= record.date)) or
                     not s.start_date) and
                    ((s.end_date and (s.end_date >= record.date)) or
                     not s.end_date))).mapped("stop_id")

    @api.multi
    @api.depends("type", "low_stop_id.route_id.direction")
    def _compute_allowed_high_stop_ids(self):
        stop_obj = self.env["fleet.route.stop"]
        for record in self.filtered(lambda r: r.type in ("high", "change")):
            domain = []
            if record.type == "change":
                domain = [
                    ("route_id.direction", "=",
                     record.low_stop_id.route_id.direction),
                    ("id", "!=", record.low_stop_id.id)]
            record.allowed_high_stop_ids = stop_obj.search(domain)

    @api.multi
    @api.onchange("student_id", "type")
    def _onchange_student(self):
        self.ensure_one()
        if (self.type in ("low", "change") and
                len(self.allowed_low_stop_ids) == 1):
            self.low_stop_id = self.allowed_low_stop_ids[:1]
