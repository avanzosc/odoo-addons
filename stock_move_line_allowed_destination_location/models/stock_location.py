# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    not_allowed_as_destination = fields.Boolean(
        string="Do Not Allow Move Lines At Destination", default=False
    )
