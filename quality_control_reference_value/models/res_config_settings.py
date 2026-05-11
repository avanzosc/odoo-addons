# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quality_default_uom_id = fields.Many2one(
        "uom.uom", string="Default Unit", config_parameter="quality.default_uom_id"
    )

    quality_base_tolerance = fields.Float(
        string="Base Tolerance", default=0.2, config_parameter="quality.base_tolerance"
    )

    quality_default_type = fields.Selection(
        [
            ("qualitative", "Qualitative"),
            ("quantitative", "Quantitative"),
        ],
        string="Default Type",
        default="quantitative",
        config_parameter="quality.default_type",
    )
