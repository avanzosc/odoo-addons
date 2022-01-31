# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class BirthRate(models.Model):
    _name = "birth.rate"
    _description = "Birth Rate"

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    mother_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.production.lot')
    week = fields.Integer(string='Week')
    percentage_birth = fields.Float(string='% of Birth Over Total')
