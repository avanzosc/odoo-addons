# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class Lineage(models.Model):
    _name = "lineage"
    _description = "Lineage"

    name = fields.Char(string='Name')
    code = fields.Char(string='Code')
    birth_rate_ids = fields.One2many(
        string='Birth Rate',
        comodel_name='birth.rate',
        inverse_name='lineage_id')
    laying_rate_ids = fields.One2many(
        string='Laying Rate',
        comodel_name='laying.rate',
        inverse_name='lineage_id')
    mother_ids = fields.One2many(
        string='Mothers',
        comodel_name='stock.picking.batch',
        inverse_name='lineage_id')
