# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class AccountPaymentResigter(models.TransientModel):
    _inherit = "account.payment.register"

    @api.depends("can_edit_wizard")
    def _compute_communication(self):
        super()._compute_communication()
        for wizard in self:
            if wizard.can_edit_wizard:
                batches = wizard._get_batches()
                wizard.communication = "{} - {}".format(
                    wizard._get_batch_communication(batches[0]), self.env.user.name
                )
            else:
                wizard.communication = False
