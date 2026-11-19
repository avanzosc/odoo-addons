# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    contract_sale_generation_exception_responsible_id = fields.Many2one(
        "res.users",
        string="Sale Generation Exception Responsible",
        config_parameter="contract_sale_generation_isolation.responsible_user_id",
        help=(
            "User assigned an activity when the recurring sale order "
            "generation for a contract fails. If not set, the contract's "
            "own responsible user is used instead."
        ),
    )
