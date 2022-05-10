# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class LayingRate(models.Model):
    _name = "laying.rate"
    _description = "Laying Rate"

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    mother_id = fields.Many2one(
        string='Mother',
        comodel_name='stock.picking.batch')
    week = fields.Integer(string='Week')
    percentage_laying = fields.Float(string='% of Laying')
