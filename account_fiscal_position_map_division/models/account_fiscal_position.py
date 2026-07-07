# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    @api.depends("account_ids.account_src_id", "account_ids.account_dest_id")
    def _compute_account_map(self):
        division = self.env.context.get("division")
        if not division and self.env.context.get("active_model") == "sale.order":
            sale = self.env["sale.order"].browse(self.env.context.get("active_id"))
            division = sale.team_id.id if sale and sale.team_id else False
        result = super()._compute_account_map()

        for position in self:
            accounts = position.account_ids
            if division:
                accounts_div = accounts.filtered(lambda a: a.team_id.id == division)
                if accounts_div:
                    accounts = accounts_div
                else:
                    accounts = accounts.filtered(lambda a: not a.team_id)
            else:
                accounts = accounts.filtered(lambda a: not a.team_id)
            position.account_map = {
                al.account_src_id.id: al.account_dest_id.id for al in accounts
            }
        return result
