from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    valued = fields.Boolean(
        "Valued Picking",
        store=True,
    )
