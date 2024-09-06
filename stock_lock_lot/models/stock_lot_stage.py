from odoo import fields, models


class StockLotStage(models.Model):
    _name = "stock.lot.stage"
    _description = "Stock Lot Stage"

    name = fields.Char(
        required=True,
    )
    stage_blocking = fields.Boolean()
