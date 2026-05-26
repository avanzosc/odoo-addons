# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models
from odoo.tools import float_repr, float_round


class StockProductionLot(models.Model):
    _inherit = "stock.lot"

    @api.depends("name", "product_qty")
    @api.depends_context("default_location_id")
    def _compute_display_name(self):
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        fallback_rounding = 10**-precision
        for lot in self:
            precision_rounding = lot.product_uom_id.rounding or fallback_rounding
            lot.display_name = "{} ({})".format(
                lot.name or "",
                float_repr(
                    float_round(lot.product_qty, precision_rounding=precision_rounding),
                    precision,
                ),
            )

    @api.depends(
        "quant_ids",
        "quant_ids.quantity",
        "quant_ids.location_id",
        "quant_ids.location_id.usage",
        "quant_ids.location_id.company_id",
    )
    @api.depends_context("default_location_id")
    def _product_qty(self):
        super()._product_qty()
        location_id = self.env.context.get("default_location_id")
        if not location_id:
            return
        for lot in self:
            # We only care for the quants in internal or transit locations.
            quants = lot.quant_ids.filtered(
                lambda q: q.location_id.id == location_id
                and (
                    q.location_id.usage == "internal"
                    or (q.location_id.usage == "transit" and q.location_id.company_id)
                )
            )
            lot.product_qty = sum(quants.mapped("quantity"))
