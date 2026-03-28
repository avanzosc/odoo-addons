from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _compute_price_unit_and_date_planned_and_name(self):
        """
        This function is inherited to modify the default behavior of the method
        `_compute_price_unit_and_date_planned_and_name`. The goal is to set the
        `date_planned` field on the purchase order lines based on corresponding
        schedule dates from the related requisition lines.

        The original function computes the unit price and other details like name
        and planned date. Here, we extend it by saving the schedule dates from
        the requisition lines before calling the `super()` method. Afterward,
        we use the saved indices to assign the correct `schedule_date` to each
        purchase order line (`pol`), ensuring that the order of lines remains intact.
        """

        requisition_lines = {}
        indices = {}

        # Save requisition lines and their corresponding indices
        for index, pol in enumerate(self):
            requisition_lines[index] = pol.order_id.requisition_id.line_ids
            indices[pol.id] = index

        # Call the original method to compute price and other values
        res = super()._compute_price_unit_and_date_planned_and_name()

        # After the super method, assign the correct schedule_date to each purchase order line
        for pol in self:
            index = indices[pol.id]
            requisition_line = requisition_lines.get(index, False)
            if requisition_line:
                pol.date_planned = requisition_line[index].schedule_date
            else:
                pol.date_planned = False

        return res
