# Copyright 2025 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class HrPersonalEquipment(models.Model):
    _inherit = "hr.personal.equipment"

    job_id = fields.Many2one(
        comodel_name="hr.job",
        related="employee_id.job_id",
        store=True,
    )
