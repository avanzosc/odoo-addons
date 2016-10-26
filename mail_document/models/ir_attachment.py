# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    @api.multi
    def write(self, vals):
        for record in self:
            if vals.get('res_id', False) and vals.get('res_model', False) and\
                    not vals.get('partner_id', False):
                vals['partner_id'] =\
                    record._document_file__get_partner_id(vals['res_model'],
                                                          vals['res_id'])
            vals['description'] = self.env.context.get(
                'attachment_description', vals.get('description', ''))
            super(IrAttachment, record).write(vals)
