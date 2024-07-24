# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class WizEventAttendanceReport(models.TransientModel):
    _inherit = "wiz.event.attendance.report"

    academic_year_id = fields.Many2one(
        string="Academic year", comodel_name="event.academic.year"
    )

    @api.onchange("academic_year_id")
    def _onchange_academic_year_id(self):
        self.put_allowed_data()

    def filter_lines(self, lines):
        lines = super(WizEventAttendanceReport, self).filter_lines(lines)
        if self.academic_year_id:
            lines = lines.filtered(
                lambda x: x.academic_year_id.id == self.academic_year_id.id
            )
        return lines

    def count_num_filters(self, cont):
        cont = super(WizEventAttendanceReport, self).count_num_filters(cont)
        if self.academic_year_id:
            cont += 1
        return cont

    def get_vals_for_wizard_line(self, event, customer, vals=False):
        if not vals:
            vals = {}
        vals = super(WizEventAttendanceReport, self).get_vals_for_wizard_line(
            event, customer, vals=vals
        )
        vals["academic_year_id"] = event.academic_year_id.id
        return vals


class WizEventAttendanceReportLine(models.TransientModel):
    _inherit = "wiz.event.attendance.report.line"

    academic_year_id = fields.Many2one(
        string="Academic year", comodel_name="event.academic.year"
    )
