# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        string="Quantity On Hand",
        digits="Product Unit of Measure",
        compute="_compute_quantities",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        compute="_compute_quantities",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_quantities",
    )
    supplier_pending_to_receive = fields.Float(
        string="Pending receipt from supplier",
        related="supplier_id.supplier_pending_to_receive",
    )

    def _compute_quantities(self):
        for record in self:
            location_product = record.product_id.with_context(
                location=record.location_id.id
            )
            record.update(
                {
                    "qty_available": location_product.qty_available,
                    "incoming_qty": location_product.incoming_qty,
                    "outgoing_qty": location_product.outgoing_qty,
                }
            )
