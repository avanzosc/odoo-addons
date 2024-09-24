# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class AssignManualQuants(models.TransientModel):
    _inherit = "assign.manual.quants"

    def assign_quants(self):
        result = super().assign_quants()
        lines = self.move_id.move_line_ids.filtered(
            lambda x: not x.reserved_qty and not x.reserved_uom_qty and not x.qty_done
        )
        if lines:
            lines.unlink()
        return result
