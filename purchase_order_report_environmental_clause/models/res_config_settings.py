# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    environmental_clause_text = fields.Text(
        translate=True,
    )

    @api.model
    def get_values(self):
        res = super().get_values()
        res.update(
            environmental_clause_text=self.env["ir.config_parameter"]
            .sudo()
            .get_param("environmental_clause_text", ""),
        )
        return res

    def set_values(self):
        res = super().set_values()
        self.env["ir.config_parameter"].sudo().set_param(
            "environmental_clause_text",
            self.environmental_clause_text or "",
        )
        return res
