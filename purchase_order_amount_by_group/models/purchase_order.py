# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from functools import partial

from odoo import fields, models
from odoo.tools.misc import formatLang


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    amount_by_group = fields.Binary(
        string="Tax amount by group",
        compute="_compute_amount_by_group",
        help="type: [(name, amount, base, formated amount, formated base)]",
    )

    def _compute_amount_by_group(self):
        for order in self:
            currency = order.currency_id or order.company_id.currency_id
            fmt = partial(
                formatLang,
                self.with_context(lang=order.partner_id.lang).env,
                currency_obj=currency,
            )
            res = {}
            for line in order.order_line:
                price_reduce = line.price_unit * (1.0 - line.discount / 100.0)
                taxes = line.taxes_id.compute_all(
                    price_reduce,
                    quantity=line.product_uom_qty,
                    product=line.product_id,
                    partner=order.partner_id,
                )["taxes"]
                for tax in line.taxes_id:
                    group = tax.tax_group_id
                    res.setdefault(group, {"amount": 0.0, "base": 0.0})
                    for t in taxes:
                        if t["id"] == tax.id or t["id"] in tax.children_tax_ids.ids:
                            res[group]["amount"] += t["amount"]
                            res[group]["base"] += t["base"]
            res = sorted(res.items(), key=lambda l: l[0].sequence)
            for group_data in res:
                group_data[1]["amount"] = currency.round(group_data[1]["amount"]) + 0.0
                group_data[1]["base"] = currency.round(group_data[1]["base"]) + 0.0
            order.amount_by_group = [
                (
                    ln[0].name,
                    ln[1]["amount"],
                    ln[1]["base"],
                    fmt(ln[1]["amount"]),
                    fmt(ln[1]["base"]),
                    len(res),
                )
                for ln in res
            ]
