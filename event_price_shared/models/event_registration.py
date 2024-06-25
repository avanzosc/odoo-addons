# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class EventRegistatration(models.Model):
    _inherit = "event.registration"

    task_id = fields.Many2one(
        string="Task",
        comodel_name="project.task",
        store=True,
        related="sale_order_line_id.task_id",
    )
