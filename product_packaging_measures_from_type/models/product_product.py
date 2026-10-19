# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def write(self, vals):
        res = super().write(vals)
        if "weight" in vals and not self.env.context.get(
            "skip_packaging_weight_height_recompute"
        ):
            self.action_recalculate_packaging_weight_height()
        return res

    def action_recalculate_packaging_weight_height(self):
        for product in self:
            product._recalculate_packaging_weight_height()

    def _recalculate_packaging_weight_height(self):
        self.ensure_one()
        packagings = self.env["product.packaging"].search(
            [("product_id", "=", self.id), ("qty", ">", 0)],
            order="qty asc, id asc",
        )
        product_unit_weight = self.weight or 0.0

        for packaging in packagings:
            packaging_qty = packaging.qty
            net_weight = packaging_qty * product_unit_weight

            package_type = packaging.package_type_id
            base_weight = package_type.base_weight or 0.0
            base_height = package_type.height or 0.0

            smaller_packagings = packagings.filtered(
                lambda p: 0 < p.qty < packaging_qty
            ).sorted(key=lambda p: p.qty, reverse=True)

            inner_packaging = self.env["product.packaging"]
            inner_count = 0
            for candidate in smaller_packagings:
                ratio = packaging_qty / candidate.qty
                if abs(ratio - round(ratio)) < 0.000001:
                    inner_packaging = candidate
                    inner_count = int(round(ratio))
                    break

            is_pallet = bool(inner_packaging)

            if is_pallet:
                inner_type = inner_packaging.package_type_id
                inner_base_weight = inner_type.base_weight or 0.0
                inner_height = inner_type.height or 0.0
                inner_qty_per_layer = inner_type.qty_per_layer or 1

                weight = base_weight + net_weight + inner_count * inner_base_weight
                number_of_layers = (
                    inner_count + inner_qty_per_layer - 1
                ) // inner_qty_per_layer
                height = base_height + number_of_layers * inner_height
            else:
                weight = base_weight + net_weight
                height = base_height

            packaging.with_context(skip_packaging_weight_height_recompute=True).write(
                {"weight": weight, "height": height, "is_pallet": is_pallet}
            )
