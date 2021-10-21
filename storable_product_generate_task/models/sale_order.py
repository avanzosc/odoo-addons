# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def _action_confirm(self):
        result = super(SaleOrder, self)._action_confirm()
        self.treatment_storable_product_generate_task()
        return result

    def treatment_storable_product_generate_task(self):
        for order in self:
            lines = order.order_line.filtered(
                lambda x: x.product_id.type == 'product' and
                x.product_id.service_tracking != 'no' and
                x.state == 'sale' and not x.is_expense and not x.is_service)
            if lines:
                lines.write({'is_service': True})
                for line in lines:
                    line.sudo().with_context(
                        default_company_id=order.company_id.id,
                        force_company=order.company_id.id,
                        )._timesheet_service_generation()
