# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class QcInspectionLine(models.Model):
    _inherit = "qc.inspection.line"

    reference = fields.Char(string="Reference")
