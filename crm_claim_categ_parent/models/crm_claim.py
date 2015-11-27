# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    section_id = fields.Many2one(
        comodel_name='crm.case.section', string='Sales Team')

    @api.multi
    @api.onchange('categ_id')
    def onchange_categ_id(self):
        self.ensure_one()
        self.section_id = self.categ_id.section_id
