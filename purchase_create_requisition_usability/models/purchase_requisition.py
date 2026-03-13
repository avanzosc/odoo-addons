# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.model_create_multi
    def create(self, vals_list):
        requisitions = super().create(vals_list)
        purchase_ids = self.env.context.get("default_purchase_order_ids")
        if not purchase_ids:
            return requisitions

        if isinstance(purchase_ids, int):
            purchase_ids = [purchase_ids]
        elif not isinstance(purchase_ids, list | tuple | set):
            return requisitions

        purchase_ids = [
            purchase_id
            for purchase_id in purchase_ids
            if isinstance(purchase_id, int) and purchase_id > 0
        ]
        if not purchase_ids:
            return requisitions

        purchases = self.env["purchase.order"].browse(purchase_ids).exists()
        if not purchases:
            return requisitions

        for requisition in requisitions:
            line_commands = []
            req_purchases = purchases.filtered_domain(
                [("company_id", "=", requisition.company_id.id)]
            )
            for purchase in req_purchases:
                for line in purchase.order_line.filtered(
                    lambda order_line: not order_line.display_type
                ):
                    line_commands.append(
                        (
                            0,
                            0,
                            {
                                "product_id": line.product_id.id,
                                "product_qty": line.product_qty,
                                "product_uom_id": line.product_uom.id,
                                "price_unit": line.price_unit,
                            },
                        )
                    )
            if line_commands:
                requisition.write({"line_ids": line_commands})
        return requisitions
