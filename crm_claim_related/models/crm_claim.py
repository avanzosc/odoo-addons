# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class CrmClaim(models.Model):
    _inherit = 'crm.claim'

    to_related_claims = fields.Many2many(
        comodel_name="crm.claim", relation="rel_claim_claims",
        column1="claim_father_id", column2="claim_child_id",
        string="To related claims")
    from_related_claims = fields.Many2many(
        comodel_name="crm.claim", relation="rel_claim_claims",
        column1="claim_child_id", column2="claim_father_id",
        string="From related claims")
