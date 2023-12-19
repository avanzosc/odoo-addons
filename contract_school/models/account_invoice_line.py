# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    payment_percentage = fields.Float(string='Payment %', default=100.0)
    child_id = fields.Many2one(
        comodel_name="res.partner", string="Student",
        domain=[("educational_category", "=", "student")],
        related="invoice_id.child_id", store=True)
    course_id = fields.Many2one(
        comodel_name="education.course", string="Education Course",
        related="invoice_id.course_id", store=True)
    school_id = fields.Many2one(
        comodel_name="res.partner", string="Education Center",
        domain=[("educational_category", "=", "school")],
        related="invoice_id.school_id", store=True)
    academic_year_id = fields.Many2one(
        comodel_name="education.academic_year", string="Academic Year",
        related="invoice_id.academic_year_id", store=True)

    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
                 'product_id', 'invoice_id.partner_id',
                 'invoice_id.currency_id', 'invoice_id.company_id',
                 'invoice_id.date_invoice', 'invoice_id.date',
                 'payment_percentage')
    def _compute_price(self):
        for line in self:
            super(AccountInvoiceLine, line)._compute_price()
            if (line.payment_percentage > 0 and
                    line.payment_percentage != 100.0):
                percentage = line.payment_percentage / 100.0
                line.price_subtotal *= percentage
                line.price_subtotal_signed *= percentage
                line.price_total *= percentage
