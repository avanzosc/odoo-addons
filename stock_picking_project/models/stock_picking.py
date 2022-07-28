# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    task_id = fields.Many2one(
        comodel_name="project.task",
        string="Task",
        domain="[('project_id.analytic_account_id','=',analytic_account_id)]",
    )
