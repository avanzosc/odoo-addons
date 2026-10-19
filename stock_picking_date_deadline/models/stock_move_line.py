from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    date_deadline = fields.Datetime(
        related="move_id.date_deadline",
        store=True,
        readonly=True,
        string="deadline_date",
    )
