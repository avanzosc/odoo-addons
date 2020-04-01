# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class WizRunStockScheduler(models.TransientModel):
    _name = "wiz.run.stock.scheduler"
    _description = "Wizard to run manually stock scheduler"

    use_new_cursor = fields.Boolean(
        string='Run in the background', default=False)

    @api.multi
    def button_run_stock_scheduler(self):
        group_obj = self.env['procurement.group']
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []
        orderpoint_obj = self.env['stock.warehouse.orderpoint']
        orderpoints = orderpoint_obj.browse(active_ids)
        for orderpoint in orderpoints:
            group_obj.with_context(
                my_orderpoint_id=orderpoint.id,
                my_product_id=orderpoint.product_id.id).sudo().run_scheduler(
                    use_new_cursor=self.use_new_cursor,
                    company_id=orderpoint.company_id.id)
