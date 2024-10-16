# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class EventAttendanceReport(models.Model):
    _inherit = "event.attendance.report"

    time_type_id = fields.Many2one(
        string="Time type", comodel_name="project.time.type", readonly="1"
    )
    session_date_time_type = fields.Char(string="Session date&Time type", readonly=1)

    def _select_event_attendace_report(self):
        select = super(EventAttendanceReport, self)._select_event_attendace_report()
        return "{}, {}".format(
            select,
            "p.id as time_type_id, "
            "to_char(t.date, 'YYYY-MM-DD') || ' ' || p.code "
            "as session_date_time_type ",
        )

    def _from_event_attendace_report(self):
        super_from = super(EventAttendanceReport, self)._from_event_attendace_report()
        return "{} {}".format(
            super_from, " inner join project_time_type p on p.id = t.time_type_id "
        )
