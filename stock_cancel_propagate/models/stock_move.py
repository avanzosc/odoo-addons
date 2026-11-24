# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = "stock.move"

    def _action_cancel(self):
        result = super()._action_cancel()
        created_production = self.mapped("created_production_id").filtered(
            lambda p: p.state != "done"
        )
        if created_production:
            created_production.action_cancel()
        return result
