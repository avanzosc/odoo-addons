# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockImmediateTransfer(models.TransientModel):
    _inherit = "stock.immediate.transfer"

    def process(self):
        result = super(StockImmediateTransfer, self).process()
        for picking in self.pick_ids:
            picking._action_change_location_production_serial()
        return result
