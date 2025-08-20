# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    supplier_creditor_id = fields.Many2one(
        string="Supplier/Creditor", comodel_name="res.partner", copy=False
    )
    warehouse_id = fields.Many2one(
        string="Warehouse", comodel_name="stock.warehouse", copy=False
    )
