# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        string="Quantity On Hand",
        digits="Product Unit of Measure",
        related="product_id.qty_available",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        related="product_id.incoming_qty",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        related="product_id.outgoing_qty",
    )
    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        related="supplier_id.supplier_pending_to_receive",
    )
