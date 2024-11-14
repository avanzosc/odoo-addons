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
        compute_sudo=False,
        help="Forecast quantity (computed as Quantity On Hand "
        "- Outgoing + Incoming)\n"
        "In a context with a single Stock Location, this includes "
        "goods stored in this location, or any of its children.",
    )
    incoming_qty = fields.Float(
        string="Incoming",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
        compute_sudo=False,
        help="Quantity of planned incoming products.\n"
        "In a context with a single Stock Location, this includes "
        "goods arriving to this Location, or any of its children.",
    )
    outgoing_qty = fields.Float(
        string="Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
        compute_sudo=False,
        help="Quantity of planned outgoing products.\n"
        "In a context with a single Stock Location, this includes "
        "goods leaving this Location, or any of its children.",
    )
    incoming_draft_qty = fields.Float(
        string="Pending Incoming",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
        compute_sudo=False,
        help="Quantity of planned incoming products including pending movements.\n"
        "In a context with a single Stock Location, this includes "
        "goods arriving to this Location, or any of its children.",
    )
    outgoing_draft_qty = fields.Float(
        string="Pending Outgoing",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
        compute_sudo=False,
        help="Quantity of planned outgoing products including pending movements.\n"
        "In a context with a single Stock Location, this includes "
        "goods leaving this Location, or any of its children.",
    )
    virtual_draft_available = fields.Float(
        string="Forecasted with Pending",
        digits="Product Unit of Measure",
        compute="_compute_location_quantities",
        help="Pending Forecast quantity (computed as Forecasted "
        "- Pending Outgoing + Pending Incoming)\n"
        "In a context with a single Stock Location, this includes "
        "goods stored in this location, or any of its children.",
    )

    @api.depends("product_id", "location_id")
    def _compute_location_quantities(self):
        replenishment_report = self.env["stock.forecasted_product_product"]
        for record in self:
            location_product = record.product_id.with_context(
                location=record.location_id.id
            )
            virtual_available = location_product.virtual_available
            draft_qty = replenishment_report._get_report_header(
                record.product_id.product_tmpl_id.ids,
                record.product_id.ids,
                record.location_id.ids,
            )["qty"]
            incoming_draft_qty = draft_qty.get("in", 0.0)
            outgoing_draft_qty = draft_qty.get("out", 0.0)
            virtual_draft_available = (
                virtual_available + incoming_draft_qty - outgoing_draft_qty
            )
            record.update(
                {
                    "virtual_available": virtual_available,
                    "incoming_qty": location_product.incoming_qty,
                    "outgoing_qty": location_product.outgoing_qty,
                    "incoming_draft_qty": incoming_draft_qty,
                    "outgoing_draft_qty": outgoing_draft_qty,
                    "virtual_draft_available": virtual_draft_available,
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
