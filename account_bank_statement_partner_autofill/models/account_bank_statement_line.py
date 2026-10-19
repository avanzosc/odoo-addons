from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get("partner_id") and vals.get("payment_ref"):
                payment_ref = vals["payment_ref"]
                journal_id = vals.get("journal_id")
                company_id = vals.get("company_id")

                domain = [
                    ("payment_ref", "=", payment_ref),
                    ("is_reconciled", "=", True),
                    ("partner_id", "!=", False),
                ]
                if journal_id:
                    domain.append(("journal_id", "=", journal_id))

                if company_id:
                    domain.append(("company_id", "=", company_id))

                previous_line = self.env["account.bank.statement.line"].search(
                    domain, order="date desc", limit=1
                )
                if previous_line:
                    vals["partner_id"] = previous_line.partner_id.id

        records = super().create(vals_list)

        return records
