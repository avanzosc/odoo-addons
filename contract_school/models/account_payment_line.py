# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")])
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course")
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")])
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year")
