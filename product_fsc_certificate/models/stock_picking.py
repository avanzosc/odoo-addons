
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_fsc_certificate = fields.Boolean(
        'Contains FSC certificate', compute="_compute_contains_fsc_products", store=True)

    def _compute_contains_fsc_products(self):
        for record in self:
            certificates = record.move_line_ids.mapped('product_id').mapped('is_fsc_certificate')
            record.is_fsc_certificate = (True in certificates)

    def recalc_fsc_certificated(self):
        self._compute_contains_fsc_products()
