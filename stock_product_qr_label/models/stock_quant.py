# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    qr_code = fields.Char(string="QR Code", compute="_compute_qr_code")

    def _compute_qr_code(self):
        for quant in self:
            qr_code = "{} {}".format(
                quant.product_id.code if quant.product_id.code else "",
                quant.lot_id.name if quant.lot_id.name else "",
            )
            quant.qr_code = qr_code
