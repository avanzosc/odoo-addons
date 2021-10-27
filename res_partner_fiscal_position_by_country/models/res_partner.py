# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('country_id', 'state_id', 'zip', 'vat')
    def _onchange_country_state_zip(self):
        fiscal_position_obj = self.env['account.fiscal.position']
        for partner in self:
            vat_required = bool(partner.vat)
            fp = fiscal_position_obj._get_fpos_by_region(
                partner.country_id.id, partner.state_id.id, partner.zip,
                vat_required)
            if fp:
                partner.property_account_position_id = fp

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        self._onchange_country_state_zip()
        return res
