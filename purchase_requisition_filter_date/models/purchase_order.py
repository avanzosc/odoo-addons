from datetime import datetime, time

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("requisition_id")
    def _onchange_requisition_id(self):
        if self.requisition_id:
            valid_lines = self.requisition_id.line_ids.filtered(
                lambda line: self.requisition_id.date_from
                <= line.schedule_date
                <= self.requisition_id.date_to
            )
            result = super()._onchange_requisition_id()
            if valid_lines:
                for sale_order_line in self.order_line:
                    matching_requisition_lines = valid_lines.filtered(
                        lambda line: line.product_id == sale_order_line.product_id
                    )
                    if matching_requisition_lines:
                        matching_requisition_line = matching_requisition_lines[0]
                        schedule_datetime = datetime.combine(
                            matching_requisition_line.schedule_date, time.min
                        )
                        sale_order_line.date_planned = schedule_datetime
                        self.order_line = self.order_line - sale_order_line
                        self.order_line |= sale_order_line
                    else:
                        self.order_line = self.order_line - sale_order_line
                return result
