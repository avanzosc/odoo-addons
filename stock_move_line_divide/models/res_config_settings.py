# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    name_packages_by_reference = fields.Boolean(
        string="Name packages by reference",
        config_parameter="stock.name_packages_by_reference",
    )
