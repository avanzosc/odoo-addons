# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models

from odoo.addons.cleaning_database_operations.models.cleaning_database import (
    CLEANUP_TABLE_LABELS,
)

CLEANUP_TABLE_LABELS.update(
    {
        "account_asset_line": "Asset Lines",
        "account_asset": "Assets",
    }
)


class CleaningDatabase(models.Model):
    _inherit = "cleaning.database"

    def _delete_asset_operations(self):
        self.ensure_one()

        self._delete_company_table("account_asset_line")
        self._delete_company_table("account_asset")

    def _delete_accounting_operations(self):
        result = super()._delete_accounting_operations()
        self._delete_asset_operations()
        return result

    def action_delete_asset_operations(self):
        self.ensure_one()

        self._delete_asset_operations()
        self.env.invalidate_all()

        return True
