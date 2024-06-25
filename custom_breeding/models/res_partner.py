# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    leaving_date = fields.Date(string="Leaving Date")
    eurowin_account = fields.Char(string="Eurowin Account")
    account_journal_id = fields.Many2one(
        string="Journal",
        comodel_name="account.journal",
        domain=[("type", "=", "purchase")],
    )
