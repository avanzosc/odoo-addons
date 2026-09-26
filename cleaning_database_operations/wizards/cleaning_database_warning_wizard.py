# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class CleaningDatabaseWarningWizard(models.TransientModel):
    _name = "cleaning.database.warning.wizard"
    _description = "Wizard for warning when cleaning database operations"

    text = fields.Text()
    object_to_delete = fields.Selection(
        selection=[
            ("stock", "Stock"),
            ("lot", "Lot"),
            ("valuation", "Valuation Layer"),
            ("sale", "Sale"),
            ("purchase", "Purchase"),
            ("accounting", "Accounting"),
            ("sequences", "Sequences"),
        ],
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        res.update(
            {
                "text": _(
                    "Are you sure you want to delete the entire "
                    "operation? This action will be irreversible"
                )
            }
        )
        return res

    def continue_with_cleaning_database(self):
        self.ensure_one()
        cleaning_database = self.env["cleaning.database"].browse(
            self.env.context.get("active_id")
        )
        if self.object_to_delete == "sale":
            return cleaning_database.action_delete_sale_operations()
        elif self.object_to_delete == "purchase":
            return cleaning_database.action_delete_purchase_operations()
        elif self.object_to_delete == "stock":
            return cleaning_database.action_delete_stock_operations()
        elif self.object_to_delete == "lot":
            return cleaning_database.action_delete_stock_production_lot()
        elif self.object_to_delete == "valuation":
            return cleaning_database.action_delete_stock_valuation_operations()
        elif self.object_to_delete == "accounting":
            return cleaning_database.action_delete_accounting_operations()
        elif self.object_to_delete == "sequences":
            return cleaning_database.action_delete_sequance_operations()
