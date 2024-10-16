# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizEventAttendanceReport(models.TransientModel):
    _inherit = "wiz.event.attendance.report"

    allowed_time_type_ids = fields.Many2many(
        string="Allowed time types",
        comodel_name="hr.project.time.type",
        relation="rel_wiz_event_attendance_report_time_type",
        column1="wiz_id",
        column2="allowed_lang_id",
    )
    time_type_id = fields.Many2one(string="Time type", comodel_name="project.time.type")

    @api.onchange("time_type_id")
    def _onchange_time_type_id(self):
        self.put_allowed_data()

    def set_allowed_data(self):
        lines = super(WizEventAttendanceReport, self).set_allowed_data()
        time_types = lines.mapped("time_type_id")
        self.allowed_time_type_ids = [(6, 0, time_types.ids)]
        return lines

    def filter_lines(self, lines):
        lines = super(WizEventAttendanceReport, self).filter_lines(lines)
        if self.time_type_id:
            lines = lines.filtered(lambda x: x.time_type_id.id == self.time_type_id.id)
        return lines

    def count_num_filters(self, cont):
        cont = super(WizEventAttendanceReport, self).count_num_filters(cont)
        if self.time_type_id:
            cont += 1
        return cont
