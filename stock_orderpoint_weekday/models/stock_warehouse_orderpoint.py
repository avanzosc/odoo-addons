# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models
from odoo.tools import float_compare


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    weekday_ids = fields.One2many(
        comodel_name="stock.warehouse.orderpoint.weekday",
        inverse_name="orderpoint_id",
        string="Weekdays Special Order",
    )

    def _get_weekday(self, today=False):
        self.ensure_one()
        if not today:
            today = fields.Date.context_today(self)
        weekdays = self.weekday_ids.filtered(
            lambda w: w.type_update == "specific" and w.specific_day == today
        )
        if not weekdays:
            weekdays = self.weekday_ids.filtered(
                lambda w: w.type_update == "weekday"
                and w.weekday == str(today.isoweekday())
            )
        return weekdays and weekdays[0]

    @api.depends(
        "qty_multiple",
        "qty_forecast",
        "product_min_qty",
        "product_max_qty",
        "weekday_ids",
        "weekday_ids.type_update",
        "weekday_ids.specific_day",
        "weekday_ids.weekday",
        "weekday_ids.quantity",
        "weekday_ids.factor",
    )
    def _compute_qty_to_order(self):
        super()._compute_qty_to_order()
        for orderpoint in self.filtered("weekday_ids"):
            update = orderpoint.qty_to_order
            rounding = orderpoint.product_uom.rounding
            weekday = orderpoint._get_weekday()
            if weekday:
                if weekday.quantity:
                    if (
                        float_compare(
                            orderpoint.qty_forecast,
                            weekday.quantity,
                            precision_rounding=rounding,
                        )
                        < 0
                    ):
                        update = weekday.quantity - orderpoint.qty_forecast
                        remainder = (
                            orderpoint.qty_multiple > 0
                            and update % orderpoint.qty_multiple
                            or 0.0
                        )
                        if (
                            float_compare(remainder, 0.0, precision_rounding=rounding)
                            > 0
                        ):
                            update += orderpoint.qty_multiple - remainder
                else:
                    update = orderpoint.qty_to_order * weekday.factor
                orderpoint.qty_to_order = update

    def _post_process_scheduler(self):
        update_date = self.env.context.get("update_date")
        result = super()._post_process_scheduler()
        if update_date:
            for orderpoint in self:
                weekday = orderpoint._get_weekday()
                if weekday and weekday.type_update == "specific":
                    weekday.specific_day = weekday.specific_day + relativedelta(years=1)
        return result
