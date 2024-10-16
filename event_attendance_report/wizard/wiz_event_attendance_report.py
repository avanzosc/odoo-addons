# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizEventAttendanceReport(models.TransientModel):
    _name = "wiz.event.attendance.report"
    _description = "Wizard for event attendance report"

    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner")
    event_id = fields.Many2one(string="Event", comodel_name="event.event")
    student_id = fields.Many2one(string="Student", comodel_name="res.partner")
    date_begin = fields.Date(string="Session Start Date")
    date_end = fields.Date(string="Session End Date")
    allowed_customer_ids = fields.Many2many(
        string="Allowed customers",
        comodel_name="res.partner",
        relation="rel_wiz_event_attendance_report_customer",
        column1="wiz_id",
        column2="allowed_customer_id",
    )
    allowed_event_ids = fields.Many2many(
        string="Allowed events",
        comodel_name="event.event",
        relation="rel_wiz_event_attendance_report_event",
        column1="wiz_id",
        column2="allowed_event_id",
    )
    allowed_student_ids = fields.Many2many(
        string="Allowed students",
        comodel_name="res.partner",
        relation="rel_wiz_event_attendance_report_student",
        column1="wiz_id",
        column2="allowed_student_id",
    )
    wizard_line_ids = fields.One2many(
        string="Wizard lines",
        comodel_name="wiz.event.attendance.report.line",
        inverse_name="wiz_id",
    )

    @api.model
    def default_get(self, fields_list):
        res = super(WizEventAttendanceReport, self).default_get(fields_list)
        lines = self.env["event.attendance.report"].search([])
        if lines:
            res.update(
                {
                    "allowed_customer_ids": [(6, 0, lines.mapped("customer_id").ids)],
                    "allowed_event_ids": [(6, 0, lines.mapped("event_id").ids)],
                    "allowed_student_ids": [(6, 0, lines.mapped("student_id").ids)],
                }
            )
        return res

    @api.onchange("customer_id")
    def _onchange_customer_id(self):
        self.put_allowed_data()

    @api.onchange("event_id")
    def _onchange_event_id(self):
        self.put_allowed_data()

    @api.onchange("student_id")
    def _onchange_student_id(self):
        self.put_allowed_data()

    @api.onchange("date_begin", "date_end")
    def _onchange_dates(self):
        self.put_allowed_data()

    def put_allowed_data(self):
        lines = self.set_allowed_data()
        self.wizard_line_ids = [(6, 0, [])]
        num_filters_to_show_wiz_lines = self.num_filters_to_show_wizard_lines()
        num_filters = self.count_num_filters(0)
        if num_filters > num_filters_to_show_wiz_lines:
            self.update_wizard_lines(lines)

    def set_allowed_data(self):
        lines = self.env["event.attendance.report"].search([])
        lines = self.filter_lines(lines)
        customers = lines.mapped("customer_id")
        events = lines.mapped("event_id")
        students = lines.mapped("student_id")
        self.allowed_customer_ids = [(6, 0, customers.ids)]
        self.allowed_event_ids = [(6, 0, events.ids)]
        self.allowed_student_ids = [(6, 0, students.ids)]
        return lines

    def filter_lines(self, lines):
        if self.customer_id:
            lines = lines.filtered(lambda x: x.customer_id.id == self.customer_id.id)
        if self.event_id:
            lines = lines.filtered(lambda x: x.event_id.id == self.event_id.id)
        if self.student_id:
            lines = lines.filtered(lambda x: x.student_id.id == self.student_id.id)
        if self.date_begin:
            lines = lines.filtered(lambda x: x.session_date >= self.date_begin)
        if self.date_end:
            lines = lines.filtered(lambda x: x.session_date >= self.date_end)
        return lines

    def num_filters_to_show_wizard_lines(self):
        return 1

    def count_num_filters(self, cont):
        if self.customer_id:
            cont += 1
        if self.event_id:
            cont += 1
        if self.student_id:
            cont += 1
        if self.date_begin:
            cont += 1
        if self.date_end:
            cont += 1
        return cont

    def update_wizard_lines(self, final_lines):
        lines = []
        events = final_lines.mapped("event_id")
        for event in events:
            event_lines = final_lines.filtered(lambda x: x.event_id == event)
            customers = event_lines.mapped("customer_id")
            for customer in customers:
                vals = self.get_vals_for_wizard_line(event, customer, {})
                lines.append((0, 0, vals))
        if lines:
            self.wizard_line_ids = lines

    def get_vals_for_wizard_line(self, event, customer, vals):
        vals.update({"event_id": event.id, "customer_id": customer.id})
        return vals

    def action_print(self):
        self.ensure_one()
        self.set_allowed_data()


class WizAttendanceActivityReportLine(models.TransientModel):
    _name = "wiz.event.attendance.report.line"
    _description = "Lines of wizard for event attendance report"
    _order = "event_name, customer_name"

    wiz_id = fields.Many2one(
        string="Wizard", comodel_name="wiz.event.attendance.report"
    )
    event_id = fields.Many2one(string="Event", comodel_name="event.event")
    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner")
