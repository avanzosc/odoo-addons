# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class MotherLineageRelation(models.Model):
    _name = "mother.lineage.relation"
    _description = "Mother-Lineage relation of a breeding"

    breeding_id = fields.Many2one(string="Breeding", comodel_name="stock.picking.batch")
    mother_id = fields.Many2one(string="Mother", comodel_name="stock.picking.batch")
    lineage_id = fields.Many2one(
        string="Lineage",
        comodel_name="lineage",
        related="mother_id.lineage_id",
        store=True,
    )
    percentage = fields.Float(string="Mother %")
