# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models
from dateutil.relativedelta import relativedelta


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    weekday_ids = fields.One2many(
        comodel_name="stock.warehouse.orderpoint.weekday",
        inverse_name="orderpoint_id", string="Weekdays Special Order")

    def _compute_qty_to_order(self):
        super(StockWarehouseOrderpoint, self)._compute_qty_to_order()
        today = fields.Date.context_today(self)
        for orderpoint in self:
            if orderpoint.weekday_ids:
                for weekday in orderpoint.weekday_ids:
                    if weekday.type_update == 'weekday' and \
                            weekday.weekday == str(today.isoweekday()):
                        if weekday.quantity:
                            update = weekday.quantity
                        elif weekday.factor:
                            update = orderpoint.qty_to_order * weekday.factor
                        orderpoint.qty_to_order = update
                    elif weekday.type_update == 'specific' and \
                            weekday.specific_day == today:
                        if weekday.quantity:
                            update = weekday.quantity
                        elif weekday.factor:
                            update = orderpoint.qty_to_order * weekday.factor
                        orderpoint.qty_to_order = update
                        weekday.specific_day = today + relativedelta(years=1)
