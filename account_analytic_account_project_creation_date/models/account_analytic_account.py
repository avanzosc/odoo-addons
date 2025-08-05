# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models

from .._common import _get_local_date


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    project_create_date = fields.Date(
        compute="_compute_project_creation_date", store=True, copy=False
    )

    @api.depends("project_ids")
    def _compute_project_creation_date(self):
        for account in self:
            account.project_create_date = (
                False
                if not account.project_ids
                else _get_local_date(
                    account.project_ids[0].create_date, self.env.user.tz
                )
            )
