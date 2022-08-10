# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    def action_show_details(self):
        self.ensure_one()
        action = super(StockMove, self).action_show_details()
        if self.raw_material_production_id:
            action["context"]["active_mo_id"] = self.raw_material_production_id
        return action
