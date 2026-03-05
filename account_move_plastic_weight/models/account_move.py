# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields

class AccountMove(models.Model):
    _inherit = "account.move"

    x_plastic_weight_non_recyclable_total = fields.Float(
        string="Total non-recycled plastic (kg)",
        store=True,
        copy=True,
        help="Sum of the weight of non-recycled plastic (subject to IPNR) of all products on the invoice.",
    )
    x_plastic_weight_recyclable_total = fields.Float(
        string="Total recycled plastic (kg)",
        store=True,
        copy=True,
        help="Sum of the weight of recycled plastic (NOT subject to IPNR) of all products on the invoice.",
    )

    def _compute_plastic_weight_totals(self):
        for move in self:
            if move.move_type not in ("out_invoice", "out_refund", "in_invoice", "in_refund"):
                continue

            total_non_recyclable = 0.0
            total_recyclable = 0.0

            for line in move.invoice_line_ids:
                if line.display_type in ("line_section", "line_note"):
                    continue
                if not line.product_id:
                    continue

                qty = line.quantity or 0.0
                if not qty:
                    continue

                try:
                    qty = line.product_uom_id._compute_quantity(qty, line.product_id.uom_id)
                except Exception:
                    qty = line.quantity

                weight_non_recyclable = line.product_id.plastic_weight_non_recyclable or 0.0
                weight_total = line.product_id.plastic_tax_weight or 0.0
                weight_recyclable = max(weight_total - weight_non_recyclable, 0.0)

                total_non_recyclable += qty * weight_non_recyclable
                total_recyclable += qty * weight_recyclable

            if move.move_type == "out_refund":
                total_non_recyclable *= -1.0
                total_recyclable *= -1.0

            move.write({
                "x_plastic_weight_non_recyclable_total": round(total_non_recyclable, 6),
                "x_plastic_weight_recyclable_total": round(total_recyclable, 6),
            })
            
    def write(self, vals):
        res = super().write(vals)
        if "invoice_line_ids" in vals:
            self._compute_plastic_weight_totals()
        return res

    def action_post(self):
        res = super().action_post()
        self._compute_plastic_weight_totals()
        return res