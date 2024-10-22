# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    def catch_values_from_create_repair_from_picking(self):
        vals = super().catch_values_from_create_repair_from_picking()
        if self.picking_id.sale_order_id.partner_invoice_id:
            vals["partner_invoice_id"] = (
                self.picking_id.sale_order_id.partner_invoice_id.id
            )
        return vals
