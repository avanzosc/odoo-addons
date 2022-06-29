# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class Lineage(models.Model):
    _inherit = "lineage"

    growth_rate_ids = fields.One2many(
        string="Growth Rate",
        comodel_name="growth.rate",
        inverse_name="lineage_id")
