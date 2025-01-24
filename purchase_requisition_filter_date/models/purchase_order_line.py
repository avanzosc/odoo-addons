from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_price_unit_and_date_planned_and_name(self):
        for pol in self:
            if pol.product_id.id in pol.order_id.requisition_id.line_ids.product_id.ids:
                matching_requisition_lines = (
                    pol.order_id.requisition_id.line_ids.filtered(
                        lambda line: line.product_id == pol.product_id
                    )
                )

                if len(matching_requisition_lines) == 1:
                    pol.date_planned = matching_requisition_lines[0].schedule_date
                elif len(matching_requisition_lines) > 1:
                    pol.date_planned = matching_requisition_lines[0].schedule_date
                else:
                    pol.date_planned = False

        return super()._compute_price_unit_and_date_planned_and_name()
