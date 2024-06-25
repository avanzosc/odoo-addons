# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockByBreedingWizard(models.TransientModel):
    _name = "stock.by.breeding.wizard"
    _description = "Wizard to see the actual stock of breedings"

    meat_cost = fields.Float(
        string="Meat Cost",
        required=True,
    )
    date = fields.Date(
        string="Date",
        required=True,
        default=fields.Date.today(),
    )

    def button_create_report(self):
        data = {}
        if self.date:
            data.update({"date": self.date})
        if self.meat_cost:
            data.update({"meat_cost": self.meat_cost})
        if "active_ids" in self.env.context:
            objects = self.env["stock.picking.batch"].browse(
                self.env.context.get("active_ids")
            )
            data.update({"objects": objects.ids})
        return self.env.ref(
            "batch_liquidation_report.report_stock_by_breeding_xlsx"
        ).report_action(self, data=data)
