# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import _, api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.tools import float_compare


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    weekday_ids = fields.One2many(
        comodel_name="stock.warehouse.orderpoint.weekday",
        inverse_name="orderpoint_id", string="Weekdays Special Order")

    @api.depends("qty_multiple", "qty_forecast", "product_min_qty", "product_max_qty")
    def _compute_qty_to_order(self):
        super(StockWarehouseOrderpoint, self)._compute_qty_to_order()
        today = fields.Date.context_today(self)
        for orderpoint in self.filtered("weekday_ids"):
            rounding = orderpoint.product_uom.rounding
            for weekday in orderpoint.weekday_ids:
                if (weekday.type_update == "weekday" and
                        weekday.weekday == str(today.isoweekday())):
                    if weekday.quantity:
                        if float_compare(orderpoint.qty_forecast,
                                         weekday.quantity,
                                         precision_rounding=rounding) < 0:
                            update = weekday.quantity - orderpoint.qty_forecast
                            remainder = (orderpoint.qty_multiple > 0 and
                                         update % orderpoint.qty_multiple or 0.0)
                            if float_compare(remainder, 0.0,
                                             precision_rounding=rounding) > 0:
                                update += orderpoint.qty_multiple - remainder
                    elif weekday.factor:
                        update = orderpoint.qty_to_order * weekday.factor
                    orderpoint.qty_to_order = update
                elif (weekday.type_update == "specific" and
                      weekday.specific_day == today):
                    if weekday.quantity:
                        if float_compare(orderpoint.qty_forecast,
                                         weekday.quantity,
                                         precision_rounding=rounding) < 0:
                            update = weekday.quantity - orderpoint.qty_forecast
                            remainder = (orderpoint.qty_multiple > 0 and
                                         update % orderpoint.qty_multiple or 0.0)
                            if float_compare(remainder, 0.0,
                                             precision_rounding=rounding) > 0:
                                update += orderpoint.qty_multiple - remainder
                    elif weekday.factor:
                        update = orderpoint.qty_to_order * weekday.factor
                    orderpoint.qty_to_order = update
                    weekday.specific_day = today + relativedelta(years=1)

    def open_form_view(self):
        self.ensure_one()
        view_ref = self.env["ir.model.data"].get_object_reference(
            "stock", "view_warehouse_orderpoint_form"
        )
        view_id = (view_ref and view_ref[1] or False,)
        return {
            "name": _("Reordering Rules"),
            "domain": [],
            "res_model": "stock.warehouse.orderpoint",
            "res_id": self.id,
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "view_type": "form",
            "view_id": view_id,
            "target": "current",
        }
