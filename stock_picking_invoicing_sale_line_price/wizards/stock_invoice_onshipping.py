# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockInvoiceOnshipping(models.TransientModel):
    _inherit = "stock.invoice.onshipping"

    def _get_invoice_line_values(self, moves, invoice_values, invoice):
        result = super()._get_invoice_line_values(moves, invoice_values, invoice)
        if len(moves) == 1 and moves.sale_line_id:
            result["price_unit"] = moves.sale_line_id.price_unit
        return result
