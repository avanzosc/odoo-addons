# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    current_user_id = fields.Many2one(
        # Use compute instead of related because it raises access error if the
        # user is in other company even using related_sudo
        compute="_compute_current_user_id",
        compute_sudo=True,
    )

    @api.depends("partner_id", "partner_id.user_id")
    def _compute_current_user_id(self):
        for invoice in self:
            invoice.current_user_id = invoice.partner_id.user_id
