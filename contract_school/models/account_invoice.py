# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

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

    def _prepare_tax_line_vals(self, line, tax):
        vals = super(AccountInvoice, self)._prepare_tax_line_vals(line, tax)
        if line.payment_percentage:
            percentage = line.payment_percentage / 100
            vals.update({
                'base': vals['base'] * percentage,
                'amount': vals['amount'] * percentage,
            })
        return vals

    @api.model
    def invoice_line_move_line_get(self):
        res = super(AccountInvoice, self).invoice_line_move_line_get()
        for line in res:
            line.update({
                "academic_year_id": self.academic_year_id.id,
                "school_id": self.school_id.id,
                "course_id": self.course_id.id,
                "child_id": self.child_id.id,
            })
        return res

    @api.model
    def tax_line_move_line_get(self):
        res = super(AccountInvoice, self).tax_line_move_line_get()
        for line in res:
            line.update({
                "academic_year_id": self.academic_year_id.id,
                "school_id": self.school_id.id,
                "course_id": self.course_id.id,
                "child_id": self.child_id.id,
            })
        return res
