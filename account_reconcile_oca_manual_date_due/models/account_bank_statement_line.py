# Copyright 2025 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    manual_date_due = fields.Date(
        string="Expiration Date (Manual)",
        store=False,
        default=False,
        prefetch=False,
    )

    def _get_manual_delete_vals(self):
        res = super()._get_manual_delete_vals()
        res.update({"manual_date_due": False})
        return res

    def _process_manual_reconcile_from_line(self, line):
        res = super()._process_manual_reconcile_from_line(line)
        if self.manual_line_id:
            self.manual_date_due = getattr(self.manual_line_id, "date_maturity", False)
            self._onchange_manual_reconcile_vals()
        return res

    @api.onchange("manual_date_due")
    def _onchange_manual_date_due(self):
        self._onchange_manual_reconcile_vals()

    def _get_manual_reconcile_vals(self):
        vals = super()._get_manual_reconcile_vals()
        vals["date_maturity"] = (
            fields.Date.to_string(self.manual_date_due)
            if self.manual_date_due
            else False
        )
        return vals

    def _reconcile_move_line_vals(self, line, move_id=False):
        vals = super()._reconcile_move_line_vals(line, move_id=move_id)
        if line.get("date_maturity"):
            vals["date_maturity"] = line["date_maturity"]
        elif self.manual_date_due:
            vals["date_maturity"] = self.manual_date_due
        return vals
