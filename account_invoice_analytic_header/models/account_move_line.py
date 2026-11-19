# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    analytic_account_id = fields.Many2one(
        string="Analytic account",
        comodel_name="account.analytic.account",
        compute="_compute_analytic_account_id",
        store=True,
        readonly=False,
        precompute=True,
    )

    @api.depends("move_id", "move_id.analytic_account_id")
    def _compute_analytic_account_id(self):
        for line in self:
            analytic_account = self.env["account.analytic.account"]
            if line.move_id.analytic_account_id:
                analytic_account = line.move_id.analytic_account_id.id
            line.analytic_account_id = analytic_account

    @api.onchange("analytic_account_id")
    def _onchange_analytic_account_id(self):
        if self.analytic_account_id:
            self.analytic_distribution = {self.analytic_account_id.id: 100.0}
