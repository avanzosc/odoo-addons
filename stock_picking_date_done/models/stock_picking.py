# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    custom_date_done = fields.Datetime(string="Date Realized")

    def button_validate(self):
        pickings_custom_date_done_null = self.filtered(lambda p: not p.custom_date_done)
        if pickings_custom_date_done_null:
            pickings_custom_date_done_null.write(
                {"custom_date_done": fields.Datetime.now()}
            )
        result = super().button_validate()
        for picking in self:
            picking.move_ids.write({"date": picking.custom_date_done})
            picking.move_line_ids.write({"date": picking.custom_date_done})
        return result
