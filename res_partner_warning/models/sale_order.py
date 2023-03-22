# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(SaleOrder, self).onchange_partner_id()
        if not self.partner_id:
            return result
        warnings = self._find_partner_warnings(self.partner_id)
        if warnings:
            self.note = warnings
        return result

    def _find_partner_warnings(self, partner):
        warnings = False
        if partner.sale_warn == 'no-message' and partner.parent_id:
            partner = partner.parent_id
        if partner.sale_warn and partner.sale_warn != 'no-message':
            warnings = _("- Warning: %s", partner.sale_warn_msg)
        return warnings

    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        del invoice_vals['narration']
        partner = self.env['res.partner'].browse(
            invoice_vals.get('partner_id'))
        warnings = self.env['account.move']._find_partner_warnings(partner)
        if warnings:
            invoice_vals['narration'] = warnings
        return invoice_vals
