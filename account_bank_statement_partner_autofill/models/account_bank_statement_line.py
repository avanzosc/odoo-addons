from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _update_partner_for_similar_lines(self):
        for line in self.filtered(lambda line: line.partner_id):
            similar_lines = self.env["account.bank.statement.line"].search(
                [
                    ("payment_ref", "=", line.payment_ref),
                    ("partner_id", "=", False),
                    ("journal_id", "=", line.journal_id.id),
                    ("id", "!=", line.id),
                ]
            )
            similar_lines.write({"partner_id": line.partner_id.id})

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("partner_id") and vals.get("payment_ref"):
                payment_ref = vals["payment_ref"]
                journal_id = vals.get("journal_id")

                domain = [
                    ("payment_ref", "=", payment_ref),
                    ("is_reconciled", "=", True),
                    ("partner_id", "!=", False),
                ]
                if journal_id:
                    domain.append(("journal_id", "=", journal_id))

                previous_line = self.env["account.bank.statement.line"].search(
                    domain, order="date desc", limit=1
                )
                if previous_line:
                    vals["partner_id"] = previous_line.partner_id.id

        records = super().create(vals_list)

        records._update_partner_for_similar_lines()

        return records
