# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_delivery_methods(self):
        delivery_methods = super()._get_delivery_methods()
        categories = self.partner_id._get_restriction_categories()
        return delivery_methods.filtered(
            lambda c: c._is_available_for_partner_categories(categories)
        )
