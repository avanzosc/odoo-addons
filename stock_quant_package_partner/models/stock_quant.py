from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        related="package_id.partner_id",
        store=True,
    )
