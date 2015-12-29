# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    claim_id = fields.Many2one(comodel_name='crm.claim',
                               string='Claim')
