# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountMoveLine(models.Model):
    _inherit="account.move.line"

    @api.onchange("debit")
    def _onchange_debit(self):
        for line in self:
            if line.debit:
                line.credit = 0.0

    @api.onchange("credit")
    def _onchange_credit(self):
        for line in self:
            if line.credit:
                line.debit = 0.0
