# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
"""Extend only OCA Open Items with reconciled invoices still in payment.

This extension deliberately retains Odoo's accounting residual amounts.  An
invoice settled against an outstanding payment has residual 0, even though the
payment may still be in transit to the bank.  Such an invoice is shown with a
label, but its residual remains zero and does not inflate report totals.
"""

from odoo import _, fields, models


class OpenItemsReport(models.AbstractModel):
    _inherit = "report.account_financial_report.open_items"

    def _get_in_payment_domain(
        self, account_ids, partner_ids, date_at_object, company_id, date_from
    ):
        """Restrict added lines exactly as the normal Open Items selection.

        In-payment status is current, not a historical state reconstruction.
        Use the user's local *today* for the new due-date requirement and the
        wizard's independent report cut-off for accounting entry dates.
        """
        domain = [
            ("account_id", "in", account_ids),
            ("company_id", "=", company_id),
            ("reconciled", "=", True),
            ("move_id.state", "=", "posted"),
            ("move_id.move_type", "in", ["out_invoice", "in_invoice"]),
            ("move_id.payment_state", "=", "in_payment"),
            ("date_maturity", ">", fields.Date.context_today(self)),
            ("date", "<=", date_at_object),
        ]
        if date_from:
            domain.append(("date", ">", date_from))
        if partner_ids:
            domain.append(("partner_id", "in", partner_ids))
        return domain

    def _prepare_in_payment_line(self, line, grouped_by):
        """Use OCA's Open Items line format so PDF and XLSX both work."""
        partner = self.env["res.partner"]
        if line.get("partner_id"):
            partner = partner.browse(line["partner_id"][0])

        if grouped_by == "salesperson":
            user = partner.user_id
            group_id = user.id or 0
            group_name = user.name or _("Missing Salesperson")
        elif grouped_by:
            group_id = partner.id or 0
            group_name = partner.name or _("Missing Partner")
        else:
            group_id = 0
            group_name = ""

        reference = line["ref"] or ""
        name = line["name"] or ""
        if reference == name:
            label = reference
        elif not reference:
            label = name
        elif not name:
            label = reference
        else:
            label = f"{reference} - {name}"
        label = f"{label} [{_('In payment')}]" if label else f"[{_('In payment')}]"

        currency = line.get("currency_id")
        # search_read's many2one values are (id, display_name) tuples.
        # OCA uses that display name in the same report column.
        line.update(
            {
                "date_maturity": line["date_maturity"]
                and line["date_maturity"].strftime("%d/%m/%Y"),
                "original": -line["credit"] if line["credit"] else line["debit"],
                "partner_id": partner.id or 0,
                "partner_name": partner.name or "",
                "ref_label": label,
                "journal_id": line["journal_id"][0],
                "entry_id": line["move_id"][0],
                "currency_id": currency[0] if currency else False,
                "currency_name": currency[1] if currency else False,
                "in_payment": True,
            }
        )
        return line, group_id, group_name

    def _get_data(
        self,
        account_ids,
        partner_ids,
        date_at_object,
        only_posted_moves,
        company_id,
        date_from,
        grouped_by,
    ):
        (
            move_lines,
            partners_data,
            journals_data,
            accounts_data,
            open_items_move_lines_data,
        ) = super()._get_data(
            account_ids,
            partner_ids,
            date_at_object,
            only_posted_moves,
            company_id,
            date_from,
            grouped_by,
        )

        domain = self._get_in_payment_domain(
            account_ids, partner_ids, date_at_object, company_id, date_from
        )
        existing_ids = {line["id"] for line in move_lines}
        missing_journals = set()
        missing_accounts = set()
        for line in self.env["account.move.line"].search_read(
            domain=domain, fields=self._get_ml_fields()
        ):
            # In historical reports a reconciled line might have been added
            # already by OCA's partial-reconciliation back-calculation.
            if line["id"] in existing_ids:
                continue
            existing_ids.add(line["id"])

            account_id = line["account_id"][0]
            line, group_id, group_name = self._prepare_in_payment_line(line, grouped_by)
            partners_data.setdefault(group_id, {"id": group_id, "name": group_name})
            move_lines.append(line)
            open_items_move_lines_data.setdefault(account_id, {}).setdefault(
                group_id, []
            ).append(line)
            if line["journal_id"] not in journals_data:
                missing_journals.add(line["journal_id"])
            if account_id not in accounts_data:
                missing_accounts.add(account_id)

        if missing_journals:
            journals_data.update(self._get_journals_data(list(missing_journals)))
        if missing_accounts:
            accounts_data.update(self._get_accounts_data(list(missing_accounts)))

        return (
            move_lines,
            partners_data,
            journals_data,
            accounts_data,
            open_items_move_lines_data,
        )
