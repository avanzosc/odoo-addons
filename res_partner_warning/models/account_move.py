# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        result = super(AccountMove, self)._onchange_partner_id()
        if not self.partner_id:
            return result
        warnings = self._find_partner_warnings(self.partner_id)
        if warnings:
            self.narration = warnings
        return result

    def _find_partner_warnings(self, partner):
        warnings = False
        if partner.invoice_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id
        if partner.invoice_warn and partner.invoice_warn != 'no-message':
            warnings = _("- Warning: %s", partner.invoice_warn_msg)
        return warnings
