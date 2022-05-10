# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def write(self, vals):
        result = super(StockMoveLine, self).write(vals)
        if ('with_custom_date_done' not in self.env.context and 'date' in vals):
            for line in self:
                if line.picking_id.custom_date_done:
                    line.with_context(with_custom_date_done=True).date = (
                        line.picking_id.custom_date_done)
        return result
