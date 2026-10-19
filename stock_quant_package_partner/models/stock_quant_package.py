from odoo import fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    partner_id = fields.Many2one("res.partner", string="Partner")
