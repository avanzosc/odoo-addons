# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class EventAttendanceReport(models.Model):
    _inherit = "event.attendance.report"
    _order = "academic_year, customer_name, event_name, session_date, student_name"

    academic_year = fields.Char(string="Academic year name", readonly="1")
    academic_year_id = fields.Many2one(
        string="Academic year", comodel_name="event.academic.year", readonly="1"
    )

    def _select_event_attendace_report(self):
        select = super(EventAttendanceReport, self)._select_event_attendace_report()
        return "{}, {}".format(
            select, "ay.name as academic_year, ay.id as academic_year_id"
        )

    def _from_event_attendace_report(self):
        super_from = super(EventAttendanceReport, self)._from_event_attendace_report()
        return "{} {}".format(
            super_from,
            "inner join event_academic_year ay on ay.id = t.academic_year_id ",
        )

    def _order_by_event_attendace_report(self):
        order_by = super(EventAttendanceReport, self)._order_by_event_attendace_report()
        my_order_by = "{}, {}".format("ay.name", order_by)
        return my_order_by
