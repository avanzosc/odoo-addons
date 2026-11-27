# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    legacy_liquidity_account_code = fields.Char(
        related="journal_id.default_account_id.code",
        readonly=True,
    )

    @api.model
    def get_legacy_exact_match_proposals(
        self,
        statement_line_ids,
    ):
        statement_lines = self.browse(statement_line_ids).exists()

        result = {str(line.id): False for line in statement_lines}

        for statement_line in statement_lines:
            (
                _transaction_amount,
                _transaction_currency,
                _journal_amount,
                _journal_currency,
                company_amount,
                company_currency,
            ) = statement_line._get_accounting_amounts_and_currencies()

            if company_currency.is_zero(company_amount):
                continue

            domain = statement_line._get_default_amls_matching_domain()
            if company_amount > 0:
                domain.append(("amount_residual", ">", 0))
            else:
                domain.append(("amount_residual", "<", 0))

            candidates = self.env["account.move.line"].search(
                domain,
                order="date desc, id desc",
                limit=100,
            )

            def _is_exact_candidate(
                aml,
                company_currency=company_currency,
                company_amount=company_amount,
            ):
                return company_currency.is_zero(aml.amount_residual - company_amount)

            exact_candidates = candidates.filtered(_is_exact_candidate)

            if not exact_candidates:
                continue
            if statement_line.partner_id:
                partner_id = statement_line.partner_id

                partner_candidates = exact_candidates.filtered(
                    lambda aml, partner_id=partner_id: aml.partner_id == partner_id
                )

                if partner_candidates:
                    exact_candidates = partner_candidates

            aml = exact_candidates[0]

            result[str(statement_line.id)] = {
                "id": aml.id,
                "account_code": aml.account_id.code or "",
                "date": fields.Date.to_string(aml.date),
                "name": aml.name or aml.move_id.name or "",
                "move_name": aml.move_id.name or "",
                "partner_name": aml.partner_id.display_name or "",
                "debit": aml.credit,
                "credit": aml.debit,
                "amount_residual": aml.amount_residual,
                "currency_id": aml.company_currency_id.id,
            }

        return result
