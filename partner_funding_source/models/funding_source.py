# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class FundingSource(models.Model):
    _name = 'funding.source'
    _description = 'Funding Source'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    grant = fields.Char(string='Grant')  # SUBVENCION
    soft_credit = fields.Char(string='Soft Credit')  # CREDITO BLANDO
    mixed_credit = fields.Char(string='Mixed Credit')  # CREDITO MIXTO
    partner_id = fields.Many2one(
        comodel_name='res.partner', string='Partner')
    funding_account_id = fields.Many2one(
        comodel_name='account.account', string='Funding Source Account')
    type_id = fields.Many2one(
        comodel_name='funding.source.type', string='Funding Type')


class FundingSourceType(models.Model):
    _name = 'funding.source.type'
    _description = 'Funding Source Type'

    name = fields.Char(string='Name', translate=True)
