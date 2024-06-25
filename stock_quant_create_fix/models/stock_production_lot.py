# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def action_repair_lot_location(self):
        result = False
        for lot in self:
            if lot.product_id.tracking == "serial":
                quant_internal = (
                    self.env["stock.quant"]
                    .search([("lot_id", "=", lot.id), ("quantity", ">", 0)])
                    .filtered(lambda c: c.location_id.usage == "internal")
                )
                quant_virtual = (
                    self.env["stock.quant"]
                    .search([("lot_id", "=", lot.id)])
                    .filtered(lambda c: c.location_id.usage != "internal")
                )
                if quant_internal and quant_virtual:
                    for line in quant_virtual:
                        line.sudo().unlink()
                if not quant_internal and len(quant_virtual) > 1:
                    last_quant = quant_virtual.filtered(
                        lambda c: c.location_id.usage == "customer"
                    )
                    if not last_quant:
                        last_quant = max(quant_virtual, key=lambda x: x.create_date)
                    last_quant.sudo().quantity = 1
                    result = last_quant
                    quant_virtual = quant_virtual - last_quant
                    for quant in quant_virtual:
                        quant.sudo().unlink()
        return result
