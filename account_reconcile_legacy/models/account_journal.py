# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    def action_open_legacy_reconcile(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id(
            "account_reconcile_legacy.action_bank_reconcile_legacy"
        )

        legacy_view = self.env.ref(
            "account_reconcile_legacy.view_bank_statement_line_kanban_legacy"
        )

        action.update(
            {
                "views": [(legacy_view.id, "kanban")],
                "view_id": legacy_view.id,
                "domain": [
                    ("journal_id", "=", self.id),
                    ("is_reconciled", "=", False),
                    ("checked", "=", True),
                    ("move_id.state", "=", "posted"),
                ],
                "context": {
                    **self.env.context,
                    "active_id": self.id,
                    "active_ids": self.ids,
                    "active_model": "account.journal",
                    "default_journal_id": self.id,
                    "search_default_journal_id": self.id,
                },
            }
        )

        return action
