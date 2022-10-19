# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models

_WEEKDAYS = [
    ("1", "Monday"),
    ("2", "Tuesday"),
    ("3", "Wednesday"),
    ("4", "Thursday"),
    ("5", "Friday"),
    ("6", "Saturday"),
    ("7", "Sunday"),
]


class StockWarehouseOrderpointWeekday(models.Model):
    _name = "stock.warehouse.orderpoint.weekday"
    _description = "Stock Warehouse Orderpoint Weekday"
    _order = "sequence"

    orderpoint_id = fields.Many2one(string="Orderpoint",
                                    comodel_name='stock.warehouse.orderpoint')
    company_id = fields.Many2one(
        comodel_name='res.company', related="orderpoint_id.company_id",
        string="Company", readonly=True)
    weekday = fields.Selection(
        selection=_WEEKDAYS, string="Week day",)
    specific_day = fields.Date(string="Specific Day")
    quantity = fields.Float(
        string="Quantity", digits='Product Unit of Measure', default=0.0)
    factor = fields.Float(string="Factor", default=0.0)
    type_update = fields.Selection(
        [("weekday", "Weekday"), ("specific", "Specific Day")],
        string="Update type", default="weekday")
    sequence = fields.Integer(string='Sequence')
    location_id = fields.Many2one(
        string='Location', comodel_name='stock.location', store=True,
        related='orderpoint_id.location_id')
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product', store=True,
        related='orderpoint_id.product_id')

    @api.onchange("quantity", "factor")
    def onchange_copyvalue(self):
        if self.quantity:
            self.factor = 0.0
        elif self.factor:
            self.quantity = 0
