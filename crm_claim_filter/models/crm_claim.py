# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    vat = fields.Char(string='TIN', related='partner_id.vat', readonly=True,
                      store=True)
    mobile = fields.Char(string='Mobile', related='partner_id.mobile',
                         readonly=True, store=True)
