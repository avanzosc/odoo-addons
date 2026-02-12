# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    quality_manager_id = fields.Many2one(
        string="Quality Manager",
        comodel_name="hr.employee",
    )
