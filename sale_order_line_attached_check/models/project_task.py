# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.multi
    @api.depends('service_project_sale_line',
                 'service_project_sale_line.ascribe')
    def _catch_attached(self):
        for record in self:
            record.attached = record.service_project_sale_line.attached

    attached = fields.Boolean(
        string='Attached', related='service_project_sale_line.attached',
        store=True)
