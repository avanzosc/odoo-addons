# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    lot_id = fields.Many2one(
        string="Lot/Serial Number", comodel_name="stock.production.lot"
    )
    tracking = fields.Selection(
        string="Tracking", related="product_id.tracking", store=True
    )
