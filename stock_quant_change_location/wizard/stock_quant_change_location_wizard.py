# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuantChangeLocationWizard(models.TransientModel):
    _name = "stock.quant.change.location.wizard"
    _description = "Wizard to change the location"

    location_id = fields.Many2one(
        string="New Location",
        comodel_name="stock.location",
    )

    def button_change_location(self):
        self.ensure_one()
        location = self.location_id
        quants = self.env.context["active_ids"]
        result = self.env["stock.quant"].action_change_location(
            location=location, quants=quants
        )
        return result
