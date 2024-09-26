# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    @api.onchange("expiration_date")
    def _onchange_expiration_date(self):
        result = super(StockProductionLot, self)._onchange_expiration_date()
        for lot in self:
            if lot.of_lots_ids:
                lots = lot.of_lots_ids.mapped("lot_id")
                if lots:
                    lots.write({"expiration_date": lot.expiration_date})
                    for lot in lots:
                        lot.with_context(
                            mrp_children_lot=True
                        )._onchange_expiration_date()
        return result

    def write(self, vals):
        result = super(StockProductionLot, self).write(vals)
        if "removal_date" in vals or "use_date" in vals or "alert_date" in vals:
            for lot in self:
                if lot.of_lots_ids:
                    lots = lot.of_lots_ids.mapped("lot_id")
                    childrens_lot_vals = {}
                    if vals.get("removal_date"):
                        childrens_lot_vals["removal_date"] = vals.get("removal_date")
                    if vals.get("use_date"):
                        childrens_lot_vals["use_date"] = vals.get("use_date")
                    if vals.get("alert_date"):
                        childrens_lot_vals["alert_date"] = vals.get("alert_date")
                    lots.write(childrens_lot_vals)
        return result
