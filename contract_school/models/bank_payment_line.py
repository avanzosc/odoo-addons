# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class BankPaymentLine(models.Model):
    _inherit = "bank.payment.line"

    student_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")],
        related="payment_line_ids.student_id", store=True)
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course",
        related="payment_line_ids.course_id", store=True)
    center_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")],
        related="payment_line_ids.center_id", store=True)
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year",
        related="payment_line_ids.academic_year_id", store=True)

    @api.model
    def same_fields_payment_line_and_bank_payment_line(self):
        """
        This list of fields is used both to compute the grouping
        hashcode and to copy the values from payment line
        to bank payment line
        The fields must have the same name on the 2 objects
        """
        same_fields = super(
            BankPaymentLine,
            self).same_fields_payment_line_and_bank_payment_line()
        same_fields += [
            "student_id", "course_id", "center_id", "academic_year_id"]
        return same_fields
