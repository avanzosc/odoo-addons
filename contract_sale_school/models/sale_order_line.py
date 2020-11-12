# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def create_contract_line(self):
        self.ensure_one()
        line_obj = self.sudo().env["contract.line"]
        for payer in self.payer_ids:
            line_obj.create_contract_line(
                payer.payer_id, payer.pay_percentage, self.product_id,
                self.product_uom_qty, self.price_unit, self.discount,
                self.originator_id,
                self.order_id.academic_year_id, self.order_id.school_id,
                self.order_id.course_id, self.order_id.child_id,
                sale_order=self.order_id,
                date_start=self.order_id.academic_year_id.date_start,
                date_end=self.order_id.academic_year_id.date_end,
                bank=payer.bank_id)
