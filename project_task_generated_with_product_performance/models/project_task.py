# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields
import openerp.addons.decimal_precision as dp


class ProjectTask(models.Model):
    _inherit = 'project.task'

    performance = fields.Float(
        'Performance', related='service_project_sale_line.performance')
    sale_qty = fields.Float(
        'Qty in sale line', digits_compute=dp.get_precision('Product UoS'),
        related='service_project_sale_line.product_uom_qty')

    def _moves_for_create_task_service_project(self, procurement):
        vals = super(ProjectTask, self)._moves_for_create_task_service_project(
            procurement)
        if procurement.sale_line_id.performance:
            qty = (procurement.sale_line_id.performance *
                   procurement.product_qty)
            vals.update({'planned_hours': qty,
                         'remaining_hours': qty})
        vals['date_start'] = (
            procurement.sale_line_id.order_id.project_id.date_start or
            False)
        vals['date_end'] = (
            procurement.sale_line_id.order_id.project_id.date or False)
        return vals
