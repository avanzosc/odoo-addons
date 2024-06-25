# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    payment_journal = fields.Boolean(string="Payment Journal", default=False)
