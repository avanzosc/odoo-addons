# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    manufacturing_date = fields.Date(string="Manufacturing date", copy=False)
    manufacturing_year = fields.Char(
        string="Manufacturing year",
        compute="_compute_manufacturing_year",
        store=True,
        copy=False,
    )

    @api.depends("manufacturing_date")
    def _compute_manufacturing_year(self):
        for lot in self:
            lot.manufacturing_year = (
                str(lot.manufacturing_date.year) if lot.manufacturing_date else ""
            )
