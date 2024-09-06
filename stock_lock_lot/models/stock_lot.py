from odoo import fields, models


class StockLot(models.Model):
    _inherit = "stock.production.lot"

    stage_id = fields.Many2one(
        "stock.lot.stage",
        string="Stage",
    )
