# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    default_incoterm_id = fields.Many2one(
        "account.incoterms", related="country_id.default_incoterm_id")

    @api.onchange('property_account_position_id')
    def _onchange_fiscal_position(self):
        for partner in self:
            fp = partner.property_account_position_id
            if fp and fp.update_vat:
                partner.update_partner_vat()

    @api.onchange('country_id', 'state_id', 'zip', 'vat')
    def _onchange_country_state_zip(self):
        fiscal_position_obj = self.env['account.fiscal.position']
        for partner in self:
            fp = fiscal_position_obj._get_fpos_by_country(
                partner.country_id)
            if fp:
                partner.property_account_position_id = fp
                partner._onchange_fiscal_position()

    @api.model
    def create(self, vals):
        res = super(ResPartner, self).create(vals)
        res._onchange_country_state_zip()
        return res
    #
    # @api.multi
    # def write(self, vals):
    #     res = super(ResPartner, self).write(vals)
    #     res._onchange_country_state_zip()
    #     return res

    def update_partner_vat(self):
        for partner in self:
            if partner.country_id and (not partner.vat or len(partner.vat) <= 2):
                partner.vat = partner.country_id.code
