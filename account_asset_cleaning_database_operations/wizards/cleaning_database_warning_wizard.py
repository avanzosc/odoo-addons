# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class CleaningDatabaseWarningWizard(models.TransientModel):
    _inherit = "cleaning.database.warning.wizard"

    object_to_delete = fields.Selection(
        selection_add=[
            ("asset", "Asset"),
        ],
        ondelete={"asset": "cascade"},
    )

    def continue_with_cleaning_database(self):
        super().continue_with_cleaning_database()
        cleaning_database = self.env["cleaning.database"].browse(
            self.env.context.get("active_id")
        )
        if self.object_to_delete == "asset":
            return cleaning_database.action_delete_asset_operations()
