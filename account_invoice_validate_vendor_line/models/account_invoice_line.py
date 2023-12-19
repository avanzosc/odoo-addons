# Copyright 2020 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    validate_ok = fields.Boolean(string='Validated',
                                 default=False)

    @api.multi
    def toggle_validate_ok(self):
        for record in self:
            record.validate_ok = not record.validate_ok
