# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _get_picking_names(self):
        picking_names = self.mapped("picking_id.name")
        return ", ".join(sorted(set(picking_names))) if picking_names else ""
