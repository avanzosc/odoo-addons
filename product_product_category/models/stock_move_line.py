from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    variant_categ_id = fields.Many2one(
        related="move_id.variant_categ_id",
        store=True,
        string="Variant Category",
    )
