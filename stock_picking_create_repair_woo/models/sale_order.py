# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        for sale in self.filtered(lambda x: x.is_repair):
            if not sale.count_in_picking_repairs:
                sale.action_create_in_picking_repair_from_sale_order()
        return super().action_confirm()
