# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockQuantChangeOwnerWizard(models.TransientModel):
    _name = "stock.quant.change.owner.wizard"
    _description = "Wizard to change the owner"

    owner_id = fields.Many2one(
        string="New Owner",
        comodel_name="res.partner",
    )

    def button_change_owner(self):
        self.ensure_one()
        owner = self.owner_id
        quants = self.env.context["active_ids"]
        result = self.env["stock.quant"].action_change_owner(owner=owner, quants=quants)
        return result
