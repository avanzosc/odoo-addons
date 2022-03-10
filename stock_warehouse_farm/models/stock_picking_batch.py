# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickinBatch(models.Model):
    _inherit = "stock.picking.batch"

    farmer_id = fields.Many2one(
        string='Farmer',
        comodel_name='res.partner',
        related='warehouse_id.farmer_id',
        store=True)
    tax_entity_id = fields.Many2one(
        string='Tax Entity',
        comodel_name='res.partner',
        related='warehouse_id.tax_entity_id',
        store=True)
