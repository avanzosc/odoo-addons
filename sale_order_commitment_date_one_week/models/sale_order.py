from datetime import timedelta

from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def set_commitment_date_one_week(self):
        for record in self:
            if record.date_order:
                new_commitment_date = fields.Datetime.from_string(
                    record.date_order
                ) + timedelta(days=7)
                record.commitment_date = fields.Datetime.to_string(new_commitment_date)
