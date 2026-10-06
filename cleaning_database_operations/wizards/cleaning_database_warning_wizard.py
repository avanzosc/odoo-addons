# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CleaningDatabaseWarningWizard(models.TransientModel):
    _name = "cleaning.database.warning.wizard"
    _description = "Wizard for warning when cleaning database operations"

    text = fields.Text(readonly=True)

    object_to_delete = fields.Selection(
        selection=[
            ("all", "All Operations"),
            ("stock", "Stock"),
            ("lot", "Lot"),
            ("accounting", "Accounting"),
            ("purchase", "Purchase"),
            ("sale", "Sale"),
            ("sequences", "Sequences"),
        ],
        required=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)

        object_to_delete = self.env.context.get("default_object_to_delete")

        if object_to_delete == "all":
            text = _(
                "You are about to delete all configured operational data "
                "for the selected companies.\n\n"
                "The cleanup will be performed in dependency order "
                "using batched DELETE operations.\n\n"
                "Stock Lots are NOT included in this cleanup and must be "
                "deleted separately if required.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "stock":
            text = _(
                "You are about to delete stock operations for the selected "
                "companies.\n\n"
                "The following objects will be deleted in dependency order: "
                "Stock Move Lines, Stock Valuation Layers, Stock Quants, "
                "Stock Moves and Stock Pickings.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "lot":
            text = _(
                "You are about to delete Stock Lots for the selected "
                "companies.\n\n"
                "Stock operations should be deleted before deleting lots.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "accounting":
            text = _(
                "You are about to delete accounting operations for the "
                "selected companies.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "purchase":
            text = _(
                "You are about to delete Purchase Order Lines and "
                "Purchase Orders for the selected companies.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "sale":
            text = _(
                "You are about to delete Sale Order Lines and Sale Orders "
                "for the selected companies.\n\n"
                "This operation is irreversible."
            )

        elif object_to_delete == "sequences":
            text = _(
                "You are about to reset the sequences for the selected "
                "companies.\n\n"
                "This operation is irreversible."
            )

        else:
            text = _(
                "Are you sure you want to continue? This operation is irreversible."
            )

        res["text"] = text

        return res

    def continue_with_cleaning_database(self):
        self.ensure_one()

        cleaning_database = (
            self.env["cleaning.database"]
            .browse(self.env.context.get("active_id"))
            .exists()
        )

        if not cleaning_database:
            raise UserError(_("Cleaning Database record not found."))

        actions = {
            "all": "action_delete_all_operations",
            "stock": "action_delete_stock_operations",
            "lot": "action_delete_stock_production_lot",
            "accounting": "action_delete_accounting_operations",
            "purchase": "action_delete_purchase_operations",
            "sale": "action_delete_sale_operations",
            "sequences": "action_delete_sequence_operations",
        }

        action_name = actions.get(self.object_to_delete)

        if not action_name:
            raise UserError(_("Unknown cleaning operation: %s") % self.object_to_delete)

        return getattr(cleaning_database, action_name)()
