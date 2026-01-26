# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models
from odoo.osv import expression

_logger = logging.getLogger(__name__)


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    virtual_available = fields.Float(
        string="Forecasted",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    incoming_qty2 = fields.Float(
        string="Pending Incoming",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    outgoing_qty2 = fields.Float(
        string="Pending Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    future_virtual_available = fields.Float(
        string="Forecasted with Pending",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )

    @api.depends("product_id", "location_id")
    def _compute_location_quantities(self):
        for record in self:
            if not record.product_id or not record.location_id:
                record.update(
                    {
                        "virtual_available": 0.0,
                        "incoming_qty": 0.0,
                        "outgoing_qty": 0.0,
                        "incoming_qty2": 0.0,
                        "outgoing_qty2": 0.0,
                        "future_virtual_available": 0.0,
                    }
                )
                continue

            product = record.product_id.with_context(location=record.location_id.id)
            virtual_available = product.virtual_available

            moves = self.env["stock.move"].search(
                [("product_id", "=", record.product_id.id), ("state", "=", "draft")]
            )

            res_location_id = record.location_id.id
            incoming_qty2 = sum(
                moves.filtered(
                    lambda m, loc=res_location_id: m.location_dest_id.id == loc
                ).mapped("product_qty")
            )
            outgoing_qty2 = sum(
                moves.filtered(
                    lambda m, loc=res_location_id: m.location_id.id == loc
                ).mapped("product_qty")
            )

            record.update(
                {
                    "virtual_available": virtual_available,
                    "incoming_qty": product.incoming_qty,
                    "outgoing_qty": product.outgoing_qty,
                    "incoming_qty2": incoming_qty2,
                    "outgoing_qty2": outgoing_qty2,
                    "future_virtual_available": virtual_available
                    + incoming_qty2
                    - outgoing_qty2,
                }
            )

    @api.model
    def _name_search(
        self, name="", args=None, operator="ilike", limit=100, name_get_uid=None
    ):
        domain = [
            "|",
            "|",
            ("product_id.name", operator, name),
            ("product_id.default_code", operator, name),
            ("name", operator, name),
        ]
        domain = expression.AND([domain, args])
        return super()._name_search(
            name=name,
            args=domain,
            operator=operator,
            limit=limit,
            name_get_uid=name_get_uid,
        )
