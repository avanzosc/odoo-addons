# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _update_price_unit_from_repair_data(self):
        if "repair" not in self.env.context:
            return super(
                SaleOrderLine, self)._update_price_unit_from_repair_data
        repair = self.env.context.get("repair")
        if not repair.lot_id:
            return super(
                SaleOrderLine, self)._update_price_unit_from_repair_data
        valid = False
        if (not repair.lot_id.expiration_date_without_hour and not
                repair.lot_id.warranty_repair_date):
            valid = True
        if (repair.lot_id.expiration_date_without_hour and
            fields.Date.context_today(self) <
                repair.lot_id.expiration_date_without_hour):
            valid = True
        if (repair.lot_id.warranty_repair_date and
            fields.Date.context_today(self) <
                repair.lot_id.warranty_repair_date):
            valid = True
        if not valid:
            return super(
                SaleOrderLine, self)._update_price_unit_from_repair_data
        self.price_unit = 0
