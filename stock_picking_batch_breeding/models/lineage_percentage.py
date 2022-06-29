# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class LineagePercentage(models.Model):
    _name = "lineage.percentage"
    _description = "Lineage Percentage"

    lineage_id = fields.Many2one(
        string='Lineage',
        comodel_name='lineage')
    percentage = fields.Float(string='Lineage %')
    batch_id = fields.Many2one(
        string="Breeding",
        comodel_name="stock.picking.batch",
        domain="[('batch_type', '=', 'breeding')]")
