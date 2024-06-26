# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPickingBatchCustomPackage(models.Model):
    _name = "stock.picking.batch.custom.package"
    _description = "Customized package name"
    _order = "picking_batch_id, name"

    picking_batch_id = fields.Many2one(
        string="Stock Picking Batch", comodel_name="stock.picking.batch", copy=False
    )
    name = fields.Char(string="Box name", copy=False)
    box_new_name = fields.Char(sring="New box name", copy=False)
