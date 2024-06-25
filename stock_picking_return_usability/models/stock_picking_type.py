# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    retun_picking_draft = fields.Boolean(string="Return in draft state", default=False)
