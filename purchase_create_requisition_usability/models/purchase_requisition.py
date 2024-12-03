# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    purchase_order_ids = fields.One2many(
        comodel_name="purchase.order", inverse_name="requisition_id"
    )

    @api.model
    def create(self, values):
        result = super(PurchaseRequisition, self).create(values)
        if "default_purchase_order_ids" in self.env.context:
            purchases = self.env["purchase.order"].browse(
                self.env.context["default_purchase_order_ids"]
            )
            for purchase in purchases:
                for line in purchase.order_line:
                    prl_obj = self.env["purchase.requisition.line"]
                    new_prl = prl_obj.new(
                        {
                            "product_id": line.product_id.id,
                            "price_unit": line.price_unit,
                            "requisition_id": result.id,
                            "schedule_date": line.date_planned,
                        }
                    )
                    for onchange_method in new_prl._onchange_methods["product_id"]:
                        onchange_method(new_prl)
                    vals = new_prl._convert_to_write(new_prl._cache)
                    vals.update(
                        {
                            "product_qty": line.product_qty,
                        }
                    )
                    prl_obj.create(vals)
        return result
