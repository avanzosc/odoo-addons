# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    batch_id = fields.Many2one(string="Breeding", comodel_name="stock.picking.batch")
    amount_kilo = fields.Float(
        string="Per Kilo",
        compute="_compute_amount_kilo",
        store=True,
        digits="Feep Decimal Precision",
    )
    amount_chicken = fields.Float(
        string="Per Chicken",
        compute="_compute_amount_chicken",
        store=True,
        digits="Feep Decimal Precision",
    )

    @api.depends("batch_id", "batch_id.meat_kilos", "amount")
    def _compute_amount_kilo(self):
        for line in self:
            amount_kilo = 0
            if line.batch_id and line.batch_id.meat_kilos != 0:
                amount_kilo = line.amount / line.batch_id.meat_kilos
            line.amount_kilo = amount_kilo

    @api.depends("batch_id", "batch_id.output_units", "amount")
    def _compute_amount_chicken(self):
        for line in self:
            amount_chicken = 0
            if line.batch_id and line.batch_id.output_units != 0:
                amount_chicken = line.amount / line.batch_id.output_units
            line.amount_chicken = amount_chicken
