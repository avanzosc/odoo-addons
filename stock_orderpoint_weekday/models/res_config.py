# Copyright 2025 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    update_weekday_orderpoint = fields.Boolean(
        string="Add a year to date automatically",
        related="company_id.update_weekday_orderpoint",
        readonly=False,
    )
