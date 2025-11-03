# Copyright 2025 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class AccountFiscalPosition(models.Model):
    _inherit = "account.fiscal.position"

    @api.model
    def map_accounts(self, accounts):
        division = 0
        if "division" in self.env.context and self.env.context.get("division", 0):
            division = self.env.context.get("division", 0)
        if (
            not division
            and "active_model" in self.env.context
            and self.env.context.get("active_model", "a") == "sale.order"
        ):
            sale = self.env["sale.order"].browse(self.env.context.get("active_id"))
            if sale and sale.team_id:
                division = sale.team_id.id
        ref_dict = {}
        my_accounts = self.account_ids.mapped("account_src_id")
        for my_account in my_accounts:
            if division:
                line = self.account_ids.filtered(
                    lambda x: x.account_src_id == my_account
                    and x.team_id
                    and x.team_id.id == division
                )
            if not division or not line:
                line = self.account_ids.filtered(
                    lambda x: x.account_src_id == my_account and not x.team_id
                )
            if line:
                ref_dict[line.account_src_id] = line.account_dest_id
        for key, acc in accounts.items():
            if acc in ref_dict:
                accounts[key] = ref_dict[acc]
        return accounts
