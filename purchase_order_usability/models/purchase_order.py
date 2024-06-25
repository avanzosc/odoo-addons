# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    warehouse_id = fields.Many2one(
        string="Warehouse",
        comodel_name="stock.warehouse",
        related="picking_type_id.warehouse_id",
        store=True,
    )
