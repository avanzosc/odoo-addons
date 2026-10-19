# Copyright 2025 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class UomUom(models.Model):
    _inherit = "uom.uom"

    is_unit = fields.Boolean(default=False)
