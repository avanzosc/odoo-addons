# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    user_id = fields.Many2one(
        comodel_name="res.users", string="Salesperson", index=True,
        default=lambda self: self.env.user)

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        for account in self:
            account.user_id = account.partner_id.user_id
