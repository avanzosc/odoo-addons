# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    batch_id = fields.Many2one(
        string="Mother",
        comodel_name="stock.picking.batch",
        related="lot_id.batch_id",
        store=True)
    broken = fields.Integer(string="Broken")
    waste = fields.Integer(string="Waste")
