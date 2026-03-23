# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    inventory_report_ids = fields.One2many(
        string="Inventory report",
        comodel_name="stock.quant",
        inverse_name="owner_id",
        copy=False,
    )
    count_inventory_reports = fields.Integer(
        string="Count inventory reports", compute="_compute_count_inventory_reports"
    )

    def _compute_count_inventory_reports(self):
        for partner in self:
            partner.count_inventory_reports = len(partner.inventory_report_ids)

    def action_inventory_report_from_partner(self):
        self.ensure_one()
        if not self.inventory_report_ids.ids:
            return True
        quant = self.env["stock.quant"]
        result = quant.with_context(
            search_default_internal_loc=1,
            search_default_productgroup=1,
            search_default_locationgroup=1,
        ).action_view_quants()
        result["domain"] = [("id", "in", self.inventory_report_ids.ids)]
        return result
