# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('country_id', 'state_id', 'zip', 'vat')
    def _onchange_country_state_zip(self):
        fiscal_position_obj = self.env['account.fiscal.position']
        for partner in self:
            partner.update_partner_vat()
            fp = fiscal_position_obj._get_fpos_by_country(
                partner.country_id)
            if fp:
                partner.property_account_position_id = fp

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        res._onchange_country_state_zip()
        return res

    @api.multi
    def write(self, vals):
        res = super(ResPartner, self).write(vals)
        res._onchange_country_state_zip()
        return res

    def update_partner_vat(self):
        for partner in self:
            if partner.country_id and (not partner.vat or len(partner.vat) <= 2):
                partner.vat = partner.country_id.code


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.model
    def _get_fpos_by_country(self, country=None):
        base_domain = [('auto_apply', '=', True)]
        fpos = False
        if country:
            domain_country = base_domain + [
                ('country_group_id', 'in', country.country_group_ids.ids)]
            fpos = self.search(domain_country, limit=1)
        return fpos
