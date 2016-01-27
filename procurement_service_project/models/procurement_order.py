# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    service_project_task = fields.Many2one(
        'project.task', string='Generated task from procurement')

    @api.model
    def _run(self, procurement):
        task_obj = self.env['project.task']
        route = procurement.product_id.route_ids.filtered(lambda r: r.id in [
            self.env.ref('procurement_service_project.route_serv_project').id])
        if procurement.product_id.type == 'service' and route:
            task_obj._create_task_from_procurement_service_project(procurement)
        return super(ProcurementOrder, self)._run(procurement)
