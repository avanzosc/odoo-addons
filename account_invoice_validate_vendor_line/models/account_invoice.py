# Copyright 2020 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    validate_ok = fields.Boolean(compute='_compute_validate_ok',
                                 string='Validated',
                                 store=True, compute_sudo=True)

    @api.multi
    @api.depends("invoice_line_ids", "invoice_line_ids.validate_ok")
    def _compute_validate_ok(self):
        for record in self:
            record.validate_ok = all(
                record.mapped("invoice_line_ids.validate_ok"))
