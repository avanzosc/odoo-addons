# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api, _


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.onchange('partner_id')
    def onchange_partner_id(self):
        result = super(StockPicking, self).onchange_partner_id()
        for picking in self:
            warnings = self._find_partner_warnings(picking.partner_id)
            if warnings:
                picking.note = warnings
        return result

    def _find_partner_warnings(self, partner):
        warnings = False
        if partner.picking_warn:
            if partner.picking_warn == 'no-message' and partner.parent_id:
                partner = partner.parent_id
            if partner.picking_warn != 'no-message':
                warnings = _("- Warning: %s", partner.picking_warn_msg)
        return warnings
