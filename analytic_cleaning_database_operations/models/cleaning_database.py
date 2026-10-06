# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models

from odoo.addons.cleaning_database_operations.models.cleaning_database import (
    CLEANUP_TABLE_LABELS,
)

CLEANUP_TABLE_LABELS.update(
    {
        "account_analytic_line": "Analytic Entries",
    }
)


class CleaningDatabase(models.Model):
    _inherit = "cleaning.database"

    def _delete_analytic_operations(self):
        self.ensure_one()

        self._delete_company_table("account_analytic_line")

    def _delete_accounting_operations(self):
        result = super()._delete_accounting_operations()
        self._delete_asset_operations()
        return result

    def action_delete_analytic_operations(self):
        self.ensure_one()

        self._delete_analytic_operations()
        self.env.invalidate_all()

        return True
