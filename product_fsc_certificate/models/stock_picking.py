from odoo import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_fsc_certificate = fields.Boolean(
        string="Contains FSC certificate",
        compute="_compute_contains_fsc_products",
        store=True,
    )

    @api.depends(
        "move_lines", "move_lines.product_id",
        "move_lines.product_id.is_fsc_certificate")
    def _compute_contains_fsc_products(self):
        for record in self:
            record.is_fsc_certificate = any(
                record.mapped("move_lines.product_id.is_fsc_certificate"))

