# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    import_unpaid_invoices = fields.Monetary(
        string="Invoices unpaid amount",
        compute="_compute_import_unpaid_invoices",
        groups="account.group_account_invoice,account.group_account_readonly",
    )

    def _compute_import_unpaid_invoices(self):
        invoice_report_obj = self.env["account.invoice.report"]
        for partner in self:
            partner.import_unpaid_invoices = 0
            all_partners_and_children = {}
            all_partner_ids = []
            all_partners_and_children[partner] = (
                partner.with_context(active_test=False)
                .search([("id", "child_of", partner.id)])
                .ids
            )
            all_partner_ids += all_partners_and_children[partner]
            domain = [
                ("partner_id", "in", all_partner_ids),
                ("state", "not in", ["draft", "cancel"]),
                ("payment_state", "=", "not_paid"),
                ("move_type", "in", ("out_invoice", "out_refund")),
            ]
            price_totals = invoice_report_obj.read_group(
                domain, ["price_total"], ["partner_id"]
            )
            for partner, child_ids in all_partners_and_children.items():
                partner.import_unpaid_invoices = sum(
                    price["price_total"]
                    for price in price_totals
                    if price["partner_id"][0] in child_ids
                )
