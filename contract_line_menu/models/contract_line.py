# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ContractLine(models.Model):
    _inherit = 'contract.line'

    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner',
        related='contract_id.partner_id', store=True)
    company_id = fields.Many2one(
        string='company', comodel_name='res.company',
        related='contract_id.company_id', store=True)
