from datetime import datetime, time

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("requisition_id")
    def _onchange_requisition_id(self):
        if not self.requisition_id:
            return super()._onchange_requisition_id()

        valid_lines = []
        filtered_indices = []

        for index, line in enumerate(self.requisition_id.line_ids):
            if (
                self.requisition_id.date_from
                <= line.schedule_date
                <= self.requisition_id.date_to
            ):
                valid_lines.append(line)
                filtered_indices.append(index)

        result = super()._onchange_requisition_id()

        if not valid_lines:
            return result

        indices_to_remove = []
        updated_lines = []

        order_lines_list = list(self.order_line)

        for index, sale_order_line in enumerate(order_lines_list):
            if index in filtered_indices:
                matching_index = filtered_indices.index(index)
                matching_requisition_line = valid_lines[matching_index]

                schedule_datetime = datetime.combine(
                    matching_requisition_line.schedule_date, time.min
                )
                sale_order_line.date_planned = schedule_datetime
                sale_order_line.product_qty = matching_requisition_line.product_qty
                updated_lines.append(sale_order_line)
            else:
                indices_to_remove.append(index)

        self.order_line = self.order_line.filtered(
            lambda line: order_lines_list.index(line) not in indices_to_remove
        )

        return result
