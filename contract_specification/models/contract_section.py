# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl

from odoo import fields, models


class ContractSection(models.Model):
    _name = 'contract.section'

    name = fields.Char(string='Name')
    translation_list_id = fields.Many2one(
        comodel_name='number.translation', string='Number translation list')
