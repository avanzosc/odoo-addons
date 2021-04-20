# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    child_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")])
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course")
    school_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")])
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year")

    @api.multi
    def _prepare_payment_line_vals(self, payment_order):
        self.ensure_one()
        vals = super(AccountMoveLine,
                     self)._prepare_payment_line_vals(payment_order)
        vals.update({
            "student_id": self.child_id.id,
            "course_id": self.course_id.id,
            "center_id": self.school_id.id,
            "academic_year_id": self.academic_year_id.id,
        })
        return vals
