# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class DeliveryCarrier(models.Model):
    _inherit = "delivery.carrier"

    partner_category_ids = fields.Many2many(
        comodel_name="res.partner.category",
        relation="delivery_carrier_res_partner_category_rel",
        column1="carrier_id",
        column2="category_id",
        string="Customer Tags",
        help="If set, only customers with at least one of these tags (on "
        "themselves or on their company) see this delivery method on the "
        "website.",
    )

    def _is_available_for_partner_categories(self, categories):
        self.ensure_one()
        return not self.partner_category_ids or bool(
            self.partner_category_ids & categories
        )
