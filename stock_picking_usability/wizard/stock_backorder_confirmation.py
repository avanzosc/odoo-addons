# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockBackorderConfirmation(models.TransientModel):
    _inherit = "stock.backorder.confirmation"

    warning_not_all_send = fields.Text(string="Not all send")

    @api.model
    def default_get(self, fields):
        result = super().default_get(fields)
        if "warning_not_all_send" in self.env.context:
            result["warning_not_all_send"] = self.env.context.get(
                "warning_not_all_send"
            )
        return result
