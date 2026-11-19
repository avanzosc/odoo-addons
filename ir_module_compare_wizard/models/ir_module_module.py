# Copyright 2026 Ana Juaristi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    available_version_ids = fields.Many2many(
        comodel_name="odoo.version",
        relation="module_available_version_rel",
        column1="module_id",
        column2="version_id",
        string="Available Versions",
    )
    included_in_core = fields.Boolean(string="Included in Core")
    core_version_ids = fields.Many2many(
        comodel_name="odoo.version",
        relation="module_core_version_rel",
        column1="module_id",
        column2="version_id",
        string="Core Versions",
    )
    technical_description = fields.Text()
