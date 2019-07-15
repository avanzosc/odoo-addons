# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    service_project_task = fields.Many2one(
        comodel_name='project.task', string='Generated task from procurement',
        copy=False)

    @api.multi
    def _is_procurement_service_project_task(self, procurement):
        return procurement.product_id._is_service_project() or False

    @api.model
    def _assign(self, procurement):
        res = super(ProcurementOrder, self)._assign(procurement)
        if not res:
            if self._is_procurement_service_project_task(procurement):
                return True
        return res

    @api.model
    def _run(self, procurement):
        task_obj = self.env['project.task']
        if (self._is_procurement_service_project_task(procurement) and not
                procurement.service_project_task):
            return task_obj._create_task_from_procurement_service_project(
                procurement)
        return super(ProcurementOrder, self)._run(procurement)

    @api.model
    def _check(self, procurement):
        if self._is_procurement_service_project_task(procurement):
            return (procurement.service_project_task and
                    procurement.service_project_task.stage_id.fold or False)
        return super(ProcurementOrder, self)._check(procurement)
