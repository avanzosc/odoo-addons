# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    automatic_rule = fields.Boolean(
        string="Create automatic reordering rule", default=False
    )
