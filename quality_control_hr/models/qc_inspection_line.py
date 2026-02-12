# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class QcInspectionLine(models.Model):
    _inherit = "qc.inspection.line"

    person_performs_inspection_id = fields.Many2one(
        string="Person who performed the measurement",
        comodel_name="hr.employee",
    )
    measurement_date = fields.Datetime(string="Measurement Date")
