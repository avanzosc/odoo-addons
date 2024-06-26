# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingBatchTotalBox(models.Model):
    _name = "stock.picking.batch.total.box"
    _description = "Total boxes customization"
    _order = "picking_batch_id, id"

    picking_batch_id = fields.Many2one(
        string="Stock Picking Batch", comodel_name="stock.picking.batch", copy=False
    )
    boxes_number = fields.Integer(string="Boxes number", copy=False)
    dimensions = fields.Char(sring="Dimensions", copy=False)
