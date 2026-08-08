# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project')
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task')
