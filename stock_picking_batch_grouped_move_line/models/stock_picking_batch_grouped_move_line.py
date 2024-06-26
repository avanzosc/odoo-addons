# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingWaveGroupedMoveLine(models.Model):
    _name = "stock.picking.batch.grouped.move.line"
    _description = "Detailed operations grouped in picking batch"
    _rec_name = "pickings"
    _order = "product_id, pickings"

    pickings = fields.Char(string="Pickings", copy=False)
    packages = fields.Char(string="Source package", copy=False)
    product_id = fields.Many2one(
        string="Product", comodel_name="product.product", copy=False
    )
    product_uom_id = fields.Many2one(
        string="UoM",
        comodel_name="uom.uom",
        store=True,
        copy=False,
        related="product_id.uom_id",
    )
    lots = fields.Char(string="Lots/Serial numbers", copy=False)
    owners = fields.Char(string="Owners", copy=False)
    qty_done = fields.Float(
        string="Done", digits="Product Unit of Measure", default=0.0, copy=False
    )
    location_id = fields.Many2one(
        string="Source location", comodel_name="stock.location", copy=False
    )
    location_dest_id = fields.Many2one(
        string="Destination location", comodel_name="stock.location", copy=False
    )
    result_packages = fields.Char(string="Result packages", copy=False)
