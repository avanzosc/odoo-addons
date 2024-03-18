# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api
from datetime import datetime


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def _compute_expiration_dates(self):
        for invoice in self.filtered(
                lambda x: x.type == 'out_invoice' and x.move_id):
            lines = invoice.move_id.mapped('line_ids').filtered(
                lambda x: x.credit == 0 and x.debit > 0 and
                x.date_maturity).sorted(key=lambda r: r.date_maturity)
            if lines:
                dates = lines.mapped('date_maturity')
                lit = False
                for date in dates:
                    date = fields.Date.to_string(date)
                    date = datetime.strptime(
                        date, '%Y-%m-%d').strftime("%d-%m-%Y")
                    lit = "{}, {}".format(lit, date) if lit else date
                if lit:
                    invoice.expiration_dates = lit

    @api.multi
    def _compute_have_lots(self):
        for invoice in self:
            have_lots = False
            for line in invoice.invoice_line_ids:
                if line.lot_ids:
                    have_lots = True
            invoice.have_lots = have_lots

    expiration_dates = fields.Char(
        string='Expiration dates', compute='_compute_expiration_dates')
    have_lots = fields.Boolean(
        string='Lots count', compute='_compute_have_lots')
