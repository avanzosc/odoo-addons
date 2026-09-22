# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    qr_code = fields.Char(string="QR Code", compute="_compute_qr_code")

    def _compute_qr_code(self):
        for line in self:
            qr_code = "{} {}".format(
                line.product_id.code if line.product_id.code else "",
                line.lot_id.name if line.lot_id.name else "",
            )
            line.qr_code = qr_code
