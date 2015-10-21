# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    vat = fields.Char('TIN', help='Tax Identification Number. The first 2 '
                      'characters are the country code.')

    @api.multi
    def on_change_partner_id(self, partner_id):
        """Recover VAT from partner if available."""
        result = super(CrmLead, self).on_change_partner_id(partner_id)
        if result.get('value'):
            partner = self.env['res.partner'].browse(partner_id)
            if partner.vat:
                result['value']['vat'] = partner.vat

        return result

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id=parent_id)
        partner = self.env['res.partner'].browse(partner_id)
        partner.vat = lead.vat
        return partner_id
