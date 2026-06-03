# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.tools import formatLang


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_by_group = fields.Binary(
        string="Tax amount by group",
        compute="_compute_amount_by_group",
        help="type: [(name, amount, base, formatted amount, formatted base)]",
    )

    @api.depends_context("lang")
    @api.depends("tax_totals")
    def _compute_amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            lang_env = self.with_context(lang=order.partner_id.lang).env
            tax_totals = order.tax_totals or {}
            tax_groups = [
                tax_group
                for subtotal in tax_totals.get("subtotals", [])
                for tax_group in subtotal.get("tax_groups", [])
            ]
            order.amount_by_group = [
                (
                    group["group_name"],
                    group["tax_amount_currency"],
                    group["base_amount_currency"],
                    formatLang(
                        lang_env,
                        group["tax_amount_currency"],
                        currency_obj=currency,
                    ),
                    formatLang(
                        lang_env,
                        group["base_amount_currency"],
                        currency_obj=currency,
                    ),
                    len(tax_groups),
                )
                for group in tax_groups
            ]
