# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class QcTestQuestion(models.Model):
    _inherit = "qc.test.question"

    reference = fields.Char(string="Reference")

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        default_type = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("quality.default_type", default="quantitative")
        )
        res["type"] = default_type
        if default_type == "quantitative":
            uom_id = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("quality.default_uom_id")
            )
            if uom_id:
                res["uom_id"] = int(uom_id)
        return res

    @api.onchange("type")
    def _onchange_type(self):
        if self.type == "quantitative":
            uom_id = (
                self.env["ir.config_parameter"]
                .sudo()
                .get_param("quality.default_uom_id")
            )
            if uom_id:
                self.uom_id = int(uom_id)
        else:
            self.uom_id = False

    def action_open_form(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "qc.test.question",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    @api.onchange("reference")
    def _onchange_reference(self):
        if self.type == "quantitative" and self.reference:
            try:
                reference_value = float(self.reference)
                tolerance = float(
                    self.env["ir.config_parameter"]
                    .sudo()
                    .get_param("quality.base_tolerance", default=0.2)
                )
                self.min_value = reference_value - tolerance
                self.max_value = reference_value + tolerance
            except ValueError:
                pass
