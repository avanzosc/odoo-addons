# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    cleaning_base_batch_size = fields.Integer(
        string="Base Batch Size",
        default=15,
        config_parameter="cleaning_database.base_batch_size",
        help="Default batch size for database cleaning operations.",
    )
