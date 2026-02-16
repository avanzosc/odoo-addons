# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    seized_units = fields.Integer(
        string="Seized Units",
        compute="_compute_seized_units",
        store=True,
    )
    seized_percentage = fields.Float(
        string="Seized %",
        compute="_compute_seized_percentage",
        store=True,
    )

    def _compute_seized_units(self):
        if not self.ids:
            for batch in self:
                batch.seized_units = 0
            return

        self.env.cr.execute(
            """
            SELECT breeding_id, SUM(seized_units)
            FROM mrp_production
            WHERE breeding_id = ANY(%s)
            GROUP BY breeding_id
        """,
            (self.ids,),
        )
        rows = dict(self.env.cr.fetchall())

        for batch in self:
            batch.seized_units = rows.get(batch.id, 0)

    @api.depends("seized_units", "output_units")
    def _compute_seized_percentage(self):
        for batch in self:
            seized_percentage = 0.0
            if batch.output_units:
                seized_percentage = (batch.seized_units / batch.output_units) * 100.0
            batch.seized_percentage = seized_percentage
