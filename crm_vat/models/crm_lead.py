# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    vat = fields.Char(string='VAT')

    @api.model
    def _lead_create_contact(self, lead, name, is_company, parent_id=False):
        partner_id = super(CrmLead, self)._lead_create_contact(
            lead, name, is_company, parent_id=parent_id)
        partner = self.env['res.partner'].browse(partner_id)
        partner.vat = lead.vat
        return partner_id
