# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.osv import expression


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    qty_available = fields.Float(
        string="Quantity Available",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
    )

    @api.depends("product_id", "location_id")
    def _compute_location_quantities(self):
        for record in self:
            ctx = {"location": record.location_id.id}
            quantities_dict = record.product_id.with_context(
                **ctx
            )._compute_quantities_dict(
                lot_id=None,
                owner_id=None,
                package_id=None,
                from_date=False,
                to_date=False,
            )

            record.qty_available = quantities_dict.get(record.product_id.id, {}).get(
                "qty_available", 0.0
            )
            record.incoming_qty = quantities_dict.get(record.product_id.id, {}).get(
                "incoming_qty", 0.0
            )
            record.outgoing_qty = quantities_dict.get(record.product_id.id, {}).get(
                "outgoing_qty", 0.0
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
