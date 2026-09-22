# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class GeneralLedgerReportWizard(models.TransientModel):
    _inherit = "general.ledger.report.wizard"

    advance_accounts_only = fields.Boolean(string="Advance payment accounts only")

    def _get_advance_group(self):
        self.ensure_one()

        company = self.company_id or self.env.company

        chart_template = self.env["account.chart.template"].with_company(company)

        advance_group = chart_template.ref(
            "account_group_438",
            raise_if_not_found=False,
        )

        if not advance_group:
            advance_group = self.env["account.group"].search(
                [
                    ("company_id", "=", company.root_id.id),
                    ("code_prefix_start", "=", "438"),
                    ("code_prefix_end", "=", "438"),
                ],
                limit=1,
            )

        return advance_group

    def _get_advance_accounts(self):
        self.ensure_one()

        company = self.company_id or self.env.company
        advance_group = self._get_advance_group()

        if not advance_group:
            return self.env["account.account"]

        accounts = (
            self.env["account.account"]
            .with_company(company)
            .search(
                [
                    ("company_ids", "in", company.ids),
                ]
            )
        )

        return accounts.filtered(lambda account: account.group_id == advance_group)

    @api.onchange(
        "receivable_accounts_only",
        "payable_accounts_only",
        "advance_accounts_only",
    )
    def onchange_type_accounts_only(self):
        """
        Extend the standard receivable/payable filter
        with advance accounts.
        """
        res = super().onchange_type_accounts_only()

        if self.advance_accounts_only:
            advance_accounts = self._get_advance_accounts()

            self.account_ids = self.account_ids | advance_accounts
        return res

    @api.onchange("company_id")
    def onchange_company_id(self):
        res = super().onchange_company_id()

        if self.advance_accounts_only:
            self.onchange_type_accounts_only()

        return res
