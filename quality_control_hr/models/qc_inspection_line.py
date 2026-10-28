# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class QcInspectionLine(models.Model):
    _inherit = "qc.inspection.line"

    person_performs_inspection_id = fields.Many2one(
        string="Person who performed the measurement",
        comodel_name="hr.employee",
    )
    measurement_date = fields.Datetime(string="Measurement Date")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            inspection_id = vals.get("inspection_id")

            if not inspection_id:
                continue

            inspection = self.env["qc.inspection"].browse(inspection_id)

            if (
                "person_performs_inspection_id" not in vals
                and inspection.person_performs_inspection_id
            ):
                vals[
                    "person_performs_inspection_id"
                ] = inspection.person_performs_inspection_id.id

            if "measurement_date" not in vals and inspection.measurement_date:
                vals["measurement_date"] = inspection.measurement_date

        return super().create(vals_list)
