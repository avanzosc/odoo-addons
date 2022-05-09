# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year")
    supervised_year_id = fields.Many2one(
        comodel_name="hr.employee.supervised.year", string="Supervised")
    teacher_id = fields.Many2one(
        comodel_name="hr.employee", string="Teacher")
    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student")
    family_id = fields.Many2one(
        comodel_name="res.partner", string="Family")
    state = fields.Selection(selection_add=[("done", "Done"),
                                            ("cancel", "Cancelled")])
    agenda = fields.Text(string="Agenda")
    center_id = fields.Many2one(
        string="Education Center", comodel_name="res.partner")
    course_id = fields.Many2one(
        string="Education Course", comodel_name="education.course")
    substitute_teacher_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Substitute",
    )

    @api.multi
    def action_open(self):
        self.write({
            "state": "open",
        })

    @api.multi
    def action_done(self):
        self.write({
            "state": "done"
        })

    @api.multi
    def action_cancel(self):
        self.write({
            "state": "cancel",
        })

    @api.multi
    def action_draft(self):
        self.write({
            "state": "draft",
        })

    @api.onchange("student_id")
    def _onchange_student(self):
        self.family_id = self.student_id.parent_id
        self.center_id = self.student_id.current_center_id
        self.course_id = self.student_id.current_course_id

    @api.multi
    def unlink(self):
        if any(self.filtered(lambda e: e.state != "draft")):
            raise UserError(
                _("You can not delete a meeting that it is not in 'draft' "
                  "state."))
        return super(CalendarEvent, self).unlink()
