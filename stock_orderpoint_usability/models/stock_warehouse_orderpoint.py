# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import operator as py_operator

from odoo import _, fields, models
from odoo.exceptions import UserError

OPERATORS = {
    "<": py_operator.lt,
    ">": py_operator.gt,
    "<=": py_operator.le,
    ">=": py_operator.ge,
    "=": py_operator.eq,
    "!=": py_operator.ne,
}


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    virtual_available = fields.Float(
        string="Forecaster",
        compute="_compute_virtual_available",
        digits="Product Unit of Measure",
    )

    forecaster_distinct_forecast = fields.Boolean(
        string="Forecaster distinct forecast",
        compute="_compute_forecaster_distinct_forecast",
        search="_search_forecaster_distinct_forecast",
    )

    def _compute_virtual_available(self):
        for orderpoint in self:
            virtual_available = 0
            if orderpoint.product_id and orderpoint.location_id:
                virtual_available = orderpoint.product_id.with_context(
                    location=orderpoint.location_id.id
                ).virtual_available
            orderpoint.virtual_available = virtual_available

    def _compute_forecaster_distinct_forecast(self):
        for orderpoint in self:
            orderpoint.forecaster_distinct_forecast = (
                True
                if orderpoint.virtual_available != orderpoint.qty_forecast
                else False
            )

    def _search_forecaster_distinct_forecast(self, operator, value):
        # TDE FIXME: should probably clean the search methods
        return self._search_orderpoint_forecaster_distinct_forecast(
            operator, value, "forecaster_distinct_forecast"
        )

    def _search_orderpoint_forecaster_distinct_forecast(self, operator, value, field):
        if field not in ("forecaster_distinct_forecast"):
            raise UserError(_("Invalid domain left operand %s", field))
        if operator not in ("<", ">", "=", "!=", "<=", ">="):
            raise UserError(_("Invalid domain operator %s", operator))
        if not isinstance(value, (float, int)):
            raise UserError(_("Invalid domain right operand %s", value))
        ids = []
        for orderpoint in self.with_context(prefetch_fields=False).search(
            [], order="id"
        ):
            if OPERATORS[operator](orderpoint[field], value):
                ids.append(orderpoint.id)
        return [("id", "in", ids)]

    def button_recompute_qty_to_order(self):
        fnames = ["qty_to_order"]
        for fname in fnames:
            self.env.add_to_compute(self._fields[fname], self)
        self.modified(fnames)

    def open_form_view(self):
        self.ensure_one()
        view_ref = self.env["ir.model.data"].get_object_reference(
            "stock", "view_warehouse_orderpoint_form"
        )
        view_id = (view_ref and view_ref[1] or False,)
        return {
            "name": _("Reordering Rule"),
            "domain": [],
            "res_model": "stock.warehouse.orderpoint",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "view_id": view_id,
            "target": "current",
        }
