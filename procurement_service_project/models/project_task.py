# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields


class ProjectTask(models.Model):
    _inherit = 'project.task'

    service_project_procurement = fields.Many2one(
        'procurement.order', string='Generated From Procurement')
    service_project_sale_line = fields.Many2one(
        'sale.order.line', string='Generated From Sale Line')

    def _create_task_from_procurement_service_project(self, procurement):
        project_obj = self.env['project.project']
        vals = self._moves_for_create_task_service_project(procurement)
        if procurement.sale_line_id.order_id.project_id:
            cond = [('analytic_account_id', '=',
                     procurement.sale_line_id.order_id.project_id.id)]
            project = project_obj.search(cond, limit=1)
            if project:
                vals['project_id'] = project.id
        task = self.env['project.task'].create(vals)
        procurement.service_project_task = task.id
        return task

    def _moves_for_create_task_service_project(self, procurement):
        vals = {'name': '%s:%s' % (procurement.origin or '',
                                   procurement.product_id.name),
                'date_deadline': procurement.date_planned,
                'planned_hours': procurement.product_qty,
                'remaining_hours': procurement.product_qty,
                'partner_id': procurement.sale_line_id.order_id.partner_id.id,
                'user_id': procurement.product_id.product_manager.id,
                'service_project_procurement': procurement.id,
                'service_project_sale_line':  procurement.sale_line_id.id,
                'description': procurement.name + '\n',
                'company_id': procurement.company_id.id}
        return vals
