# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.tools import float_round


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    def name_get(self):
        result = []
        rounding = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for lot in self:
            name = "{} ({})".format(
                lot.name, float_round(lot.product_qty, precision_digits=rounding)
            )
            result.append((lot.id, name))
        return result

    @api.depends("quant_ids", "quant_ids.quantity")
    def _product_qty(self):
        super()._product_qty()
        location_id = self.env.context.get("default_location_id")
        if location_id:
            for lot in self:
                # We only care for the quants in internal or transit locations.
                quants = lot.quant_ids.filtered(
                    lambda q: q.location_id.id == location_id
                    and (
                        q.location_id.usage == "internal"
                        or (
                            q.location_id.usage == "transit"
                            and q.location_id.company_id
                        )
                    )
                )
                lot.product_qty = sum(quants.mapped("quantity"))
