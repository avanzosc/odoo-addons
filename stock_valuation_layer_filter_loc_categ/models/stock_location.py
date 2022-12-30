# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockLocation(models.Model):
    _inherit = "stock.location"

    def write(self, vals):
        result = super(StockLocation, self).write(vals)
        if "not_show_in_inventory_reports" in vals:
            for location in self:
                location.put_show_in_stock_valuation_layer_report()
        return result

    def put_show_in_stock_valuation_layer_report(self):
        cond = [("stock_move_id", "!=", False),
                "|", ("location_id", "=", self.id),
                ("location_dest_id", "=", self.id)]
        layers = self.env["stock.valuation.layer"].search(cond)
        if layers:
            for layer in layers:
                not_show_location = (
                    layer.put_not_show_in_inventory_reports_info())
                layer.write(
                    {"not_show_location_in_inventory_reports":
                     not_show_location
                     })
