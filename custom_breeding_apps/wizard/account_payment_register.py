# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountPaymentResigter(models.TransientModel):
    _inherit = "account.payment.register"

    @api.depends("can_edit_wizard", "amount")
    def _compute_communication(self):
        result = super()._compute_communication()
        for wizard in self:
            if wizard.can_edit_wizard and wizard.communication:
                wizard.communication = f"{wizard.communication} - {self.env.user.name}"
        return result
