# Copyright 2019 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    count_meetings = fields.Integer(
        string="# Tutoring meetings", compute="_compute_count_meetings")

    @api.multi
    def _get_meetings_domain(self):
        self.ensure_one()
        return [
            "|", ("teacher_id", "=", self.id),
            ("substitute_teacher_id", "=", self.id),
        ]

    @api.multi
    def _compute_count_meetings(self):
        meeting_obj = self.env["calendar.event"]
        for employee in self:
            employee.count_meetings = meeting_obj.search_count(
                employee._get_meetings_domain())

    @api.multi
    def button_show_meetings(self):
        self.ensure_one()
        action = self.env.ref("calendar.action_calendar_event")
        action_dict = action.read()[0] if action else {}
        action_dict["context"] = safe_eval(
            action_dict.get("context", "{}"))
        action_dict["context"].update({
            "search_default_teacher_id": self.id,
            "default_teacher_id": self.id,
        })
        domain = expression.AND([
            self._get_meetings_domain(),
            safe_eval(action.domain or "[]")])
        action_dict.update({"domain": domain})
        return action_dict

    @api.multi
    def button_show_tutored_students(self):
        self.ensure_one()
        action_dict = super(HrEmployee, self).button_show_tutored_students()
        action = self.env.ref(
            "hr_school.action_hr_employee_supervised_year_form")
        domain = expression.OR([
            ["|", ("teacher_id", "=", self.id),
             ("current_substitute_id", "=", self.id)],
            safe_eval(action.domain or "[]")])
        action_dict.update({
            "domain": domain,
        })
        return action_dict
