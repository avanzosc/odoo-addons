# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    qr_code = fields.Char(
        string="QR Code",
        compute="_compute_qr_code"
    )

    def _compute_qr_code(self):
        for quant in self:
            qr_code = "{} {}".format(
                self.product_id.code if self.product_id.code else "",
                self.lot_id.name if self.lot_id.name else "")
            quant.qr_code = qr_code
