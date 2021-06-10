# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ContractLine(models.Model):
    _inherit = 'contract.line'
    _order = "contract_type, partner_id, sequence,id"

    contract_type = fields.Selection(
        index=True, related='contract_id.contract_type', store=True)
    partner_id = fields.Many2one(
        string='Partner', comodel_name='res.partner',
        related='contract_id.partner_id', store=True)
    journal_id = fields.Many2one(
        string="Journal", comodel_name="account.journal",
        related='contract_id.journal_id', store=True)
    pricelist_id = fields.Many2one(
        string="Pricelist", comodel_name="product.pricelist",
        related='contract_id.pricelist_id', store=True)
