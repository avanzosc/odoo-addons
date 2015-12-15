# -*- coding: utf-8 -*-
# (c) 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    input_channel = fields.Many2one(comodel_name='crm.tracking.medium',
                                    string='Input channel')
    response_channel = fields.Many2one(comodel_name='crm.tracking.medium',
                                       string='Response channel')
    source_id = fields.Many2one(comodel_name='crm.tracking.source',
                                string='Source')
