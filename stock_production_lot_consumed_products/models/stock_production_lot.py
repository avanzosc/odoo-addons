# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    of_lots_ids = fields.Many2many(
        string="OF Consumed products with lot",
        comodel_name="stock.move.line",
        compute="_compute_of_lots_ids",
    )

    def _compute_of_lots_ids(self):
        for lot in self:
            move_lines = self.env["stock.move.line"]
            cond = [("lot_producing_id", "=", lot.id)]
            production = self.env["mrp.production"].search(cond)
            if production:
                components = production.move_raw_ids.filtered(
                    lambda x: x.state == "done"
                )
                for component in components:
                    for line in component.move_line_ids.filtered(lambda z: z.lot_id):
                        if line not in move_lines:
                            move_lines += line
            lot.of_lots_ids = (
                [(6, 0, [])] if not move_lines else [(6, 0, move_lines.ids)]
            )
