# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class WizChangeTeacherCalendarEvent(models.TransientModel):
    _name = "wiz.change.teacher.calendar.event"
    _description = "Wizard for change teacher in meetings"

    from_date = fields.Date(string="From Date")
    to_date = fields.Date(string="To Date")
    substitute_teacher_id = fields.Many2one(
        string="Substitute Teacher", comodel_name="hr.employee")
    lines_ids = fields.One2many(
        string="Teachers/Students to change", inverse_name="wiz_id",
        comodel_name="wiz.change.teacher.calendar.event.line")

    @api.model
    def default_get(self, fields):
        result = super(WizChangeTeacherCalendarEvent, self).default_get(fields)
        if self.env.context.get("active_ids"):
            active_model = self.env.context.get("active_model")
            if active_model == "hr.employee.supervised.year":
                tutored = self.env[active_model].browse(
                    self.env.context.get("active_ids"))
                result.update({
                    "lines_ids": [
                        (0, 0, {
                            "tutor_per_year_id": x.id,
                            "teacher_id": x.teacher_id.id,
                            "student_id": x.student_id.id,
                            "academic_year_id": x.school_year_id.id,
                        }) for x in tutored],
                })
        return result

    @api.multi
    def change_teacher(self):
        for line in self.lines_ids:
            line.create_substitution()
        return {
            "type": "ir.actions.act_window_close",
        }


class WizChangeTeacherCalendarEventLine(models.TransientModel):
    _name = "wiz.change.teacher.calendar.event.line"
    _description = "Lines of wizard for change teacher in meetings"

    wiz_id = fields.Many2one(
        string="Teacher Substitution Wizard",
        comodel_name="wiz.change.teacher.calendar.event",
        required=True,
    )
    tutor_per_year_id = fields.Many2one(
        string="Supervised",
        comodel_name="hr.employee.supervised.year",
        required=True,
    )
    teacher_id = fields.Many2one(
        string="Teacher To Substitute",
        comodel_name="hr.employee",
        related="tutor_per_year_id.teacher_id",
    )
    student_id = fields.Many2one(
        string="Student",
        comodel_name="res.partner",
        related="tutor_per_year_id.student_id",
    )
    academic_year_id = fields.Many2one(
        string="Academic Year",
        comodel_name="education.academic_year",
        related="tutor_per_year_id.school_year_id",
    )

    @api.multi
    def create_substitution(self):
        substitution_obj = self.env["hr.employee.supervised.year.substitution"]
        for line in self:
            substitution_obj.create({
                "supervised_year_id": line.tutor_per_year_id.id,
                "from_date": line.wiz_id.from_date,
                "to_date": line.wiz_id.to_date,
                "substitute_teacher_id": line.wiz_id.substitute_teacher_id.id,
            })
