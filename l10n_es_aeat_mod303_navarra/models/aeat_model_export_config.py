# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class AeatModelExportConfig(models.Model):
    _inherit = "aeat.model.export.config"

    navarra_export = fields.Boolean(
        string="Navarra F66/F69 export",
        help="If checked, the export will generate the Navarra F66/F69 file "
        "instead of the official AEAT BOE file.",
    )


class AeatModelExportConfigLine(models.Model):
    _inherit = "aeat.model.export.config.line"

    export_type = fields.Selection(
        selection_add=[("raw_string", "Alphanumeric without case conversion")],
        ondelete={"raw_string": "cascade"},
    )
