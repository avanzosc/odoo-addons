# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class StockPicking(models.Model):
    _inherit = "stock.picking"

    project_id = fields.Many2one(
        string='Project', comodel_name='project.project', store=True,
        related='picking_type_id.project_id')
    task_id = fields.Many2one(
        string='Task', comodel_name='project.task', store=True,
        related='picking_type_id.task_id')
