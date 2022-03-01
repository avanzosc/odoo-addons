# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        self.treatment_storable_product_generate_task()
        return result

    def treatment_storable_product_generate_task(self):
        print ('99999999999999999999999999999')
        result = super(
            SaleOrder, self).treatment_storable_product_generate_task()
        for order in self:
            for line in order.order_line:
                print ('*** line: ' + str(line) + ', task: ' + str(line.task_id))
                print ('*** type: ' + str(line.product_id.type))
                print ('*** product_id.service_tracking: ' + str(line.product_id.service_tracking))
                print ('*** state: ' + str(line.state))
                print ('*** is_expense: ' + str(line.is_expense))
                print ('*** is_service: ' + str(line.is_service))
            
            
            lines = order.order_line.filtered(
                lambda x: x.product_id.type == 'product' and
                x.product_id.service_tracking != 'no' and
                x.state == 'sale' and not x.is_expense and x.task_id)
            print ('**** lines: ' + str(lines))
            for line in lines:
                if line.product_id.service_hour:
                    line.task_id.planned_hours = (
                        line.product_id.service_hour * line.product_uom_qty)
        return result
