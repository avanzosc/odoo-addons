# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class QcInspection(models.Model):
    _inherit = "qc.inspection"

    quality_manager_id = fields.Many2one(
        string="Quality Manager",
        comodel_name="hr.employee",
    )
    person_performs_inspection_id = fields.Many2one(
        string="Person who performed the measurement",
        comodel_name="hr.employee",
    )
    measurement_date = fields.Datetime(
        string="Measurement Date",
    )

    def _prepare_inspection_lines(self, test, force_fill=False):
        lines = super()._prepare_inspection_lines(test, force_fill=force_fill)
        for command in lines:
            if command[0] == 0:
                command[2].update(
                    {
                        "person_performs_inspection_id": self.person_performs_inspection_id.id
                        or False,
                        "measurement_date": self.measurement_date or False,
                    }
                )
        return lines

    @api.onchange(
        "person_performs_inspection_id",
        "measurement_date",
    )
    def _onchange_measurement_defaults(self):
        for inspection in self:
            for line in inspection.inspection_lines:
                if (
                    inspection.person_performs_inspection_id
                    and not line.person_performs_inspection_id
                ):
                    line.person_performs_inspection_id = (
                        inspection.person_performs_inspection_id
                    )

                if inspection.measurement_date and not line.measurement_date:
                    line.measurement_date = inspection.measurement_date

    def write(self, vals):
        res = super().write(vals)
        if "person_performs_inspection_id" in vals or "measurement_date" in vals:
            for inspection in self:
                for line in inspection.inspection_lines:
                    line_vals = {}
                    if (
                        inspection.person_performs_inspection_id
                        and not line.person_performs_inspection_id
                    ):
                        line_vals[
                            "person_performs_inspection_id"
                        ] = inspection.person_performs_inspection_id.id
                    if inspection.measurement_date and not line.measurement_date:
                        line_vals["measurement_date"] = inspection.measurement_date
                    if line_vals:
                        line.write(line_vals)
        return res
