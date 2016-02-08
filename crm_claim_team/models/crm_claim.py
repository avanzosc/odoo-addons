# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    @api.multi
    @api.onchange('section_id')
    def onchange_section_id(self):
        self.user_id = self.section_id.user_id

    responsible_id = fields.Many2one(related='section_id.user_id')
    member_ids = fields.Many2many(related='section_id.member_ids')
