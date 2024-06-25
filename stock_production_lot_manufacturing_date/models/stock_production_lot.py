# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockProductionLot(models.Model):
    _inherit = "stock.production.lot"

    manufacturing_date = fields.Date(string="Manufacturing date", copy=False)
    manufacturing_year = fields.Integer(
        string="Manufacturing year",
        compute="_compute_manufacturing_year",
        store=True,
        copy=False,
    )

    @api.depends("manufacturing_date")
    def _compute_manufacturing_year(self):
        for lot in self:
            manufacturing_year = 0
            if lot.manufacturing_date:
                manufacturing_year = lot.manufacturing_date.year
            lot.manufacturing_year = manufacturing_year
