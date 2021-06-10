# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, models
from odoo.exceptions import ValidationError


class AccountPaymentLine(models.Model):
    _inherit = "account.payment.line"

    @api.constrains("order_id", "move_line_id")
    def _check_duplicated_move_line(self):
        for line in self:
            duplicated = self.search([
                ("order_id", "=", line.order_id.id),
                ("move_line_id", "=", line.move_line_id.id),
                ("id", "!=", line.id),
            ])
            if duplicated:
                raise ValidationError(
                    _("You can't add twice the same journal item {}").format(
                        line.move_line_id.display_name))
