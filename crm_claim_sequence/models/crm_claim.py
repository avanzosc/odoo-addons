# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class CrmClaim(models.Model):
    _inherit = "crm.claim"

    sequence = fields.Char(
        string='Sequence', required=True, default="/", readonly=True)

    _sql_constraints = [
        ('crm_claim_unique_sequence', 'UNIQUE (sequence)',
         'The sequence must be unique!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('sequence', '/') == '/':
            vals['sequence'] = self.env['ir.sequence'].get('crm.claim')
        return super(CrmClaim, self).create(vals)
