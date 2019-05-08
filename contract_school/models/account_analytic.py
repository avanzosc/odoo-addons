# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    child_id = fields.Many2one(
        comodel_name='res.partner', string='Child',
        domain=[('educational_category', '=', 'student')])
    course_id = fields.Many2one(
        comodel_name='education.course', string='Initial school course')
    school_id = fields.Many2one(
        comodel_name='res.partner', string='School',
        domain=[('educational_category', '=', 'school')])
    academic_year_id = fields.Many2one(
        comodel_name='education.academic_year', string='Academic year')

    @api.model
    def _prepare_invoice_line(self, line, invoice_id):
        invoice = self.env['account.invoice'].browse(invoice_id)
        res = super(AccountAnalyticAccount, self)._prepare_invoice_line(
            line, invoice_id)
        res['payment_percentage'] = line.payment_percentage
        if ((line.from_date and invoice.date_invoice < line.from_date) or
                (line.to_date and invoice.date_invoice > line.to_date)):
            res = {}
        return res


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'

    payment_percentage = fields.Float(string='Percentage', default=100.0)
    from_date = fields.Date(string='Date from')
    to_date = fields.Date(string='Date to')
    user_id = fields.Many2one(
        comodel_name='res.users', string='User')
    observations = fields.Text(string='Observations')

    @api.multi
    @api.depends('quantity', 'price_unit', 'discount')
    def _compute_price_subtotal(self):
        super(AccountAnalyticInvoiceLine, self)._compute_price_subtotal()
        for line in self.filtered(lambda x: x.payment_percentage != 100.0):
            line.price_subtotal = (
                line.price_subtotal * line.payment_percentage) / 100
