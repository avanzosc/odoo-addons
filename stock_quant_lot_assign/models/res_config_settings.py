# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

from .stock_quant import DEFAULT_LOT_PREFIX, LOT_PREFIX_PARAM


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    quant_assign_lot_prefix = fields.Char(
        string="Assigned Lot Prefix",
        config_parameter=LOT_PREFIX_PARAM,
        default=DEFAULT_LOT_PREFIX,
        help="Prefix of the lots created when assigning a lot to quants "
        "without lot. A sequential number is added after it.",
    )
