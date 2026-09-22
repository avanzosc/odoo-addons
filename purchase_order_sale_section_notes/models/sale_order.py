# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        result = super().action_confirm()
        for sale in self:
            sale_lines = sale.order_line.filtered(lambda x: x.product_id)
            for sale_line in sale_lines:
                sale_line.check_sequence_notes_in_purchase()
        return result
