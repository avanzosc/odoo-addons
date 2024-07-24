# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class EventAttendanceReport(models.Model):
    _inherit = "event.attendance.report"

    lang_id = fields.Many2one(string="Language", comodel_name="hr.skill", readonly="1")
    level_id = fields.Many2one(
        string="Level", comodel_name="hr.skill.level", readonly="1"
    )

    def _select_event_attendace_report(self):
        select = super(EventAttendanceReport, self)._select_event_attendace_report()
        return "{}, {}".format(select, "l.id as lang_id, le.id as level_id")

    def _from_event_attendace_report(self):
        super_from = super(EventAttendanceReport, self)._from_event_attendace_report()
        return "{} {}".format(
            super_from,
            "inner join hr_skill l on l.id = t.lang_id "
            "inner join hr_skill_level le on le.id = t.level_id",
        )
