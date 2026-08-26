# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models
from odoo.osv import expression


class ProductProduct(models.Model):
    _inherit = "product.product"

    b2b_virtual_available = fields.Float(
        string="B2B Quantity",
        compute="_compute_b2b_quantities",
        digits="Product Unit of Measure",
        compute_sudo=True,
    )

    def _compute_b2b_quantities(self):
        locations = self.env["stock.location"].search([("for_stock_b2b", "=", True)])
        for product in self:
            b2b_virtual_available = 0.0
            for location in locations:
                b2b_virtual_available += (
                    product.with_context(location=location.id).qty_available
                    - product.with_context(
                        location=location.id, only_for_b2b=True
                    ).outgoing_qty
                )
            product.b2b_virtual_available = b2b_virtual_available

    def _get_domain_locations(self):
        (
            domain_quant_loc,
            domain_move_in_loc,
            domain_move_out_loc,
        ) = super()._get_domain_locations()
        if self.env.context.get("only_for_b2b", False):
            domain_move_out_loc = expression.AND(
                [domain_move_out_loc, [("location_dest_id.usage", "=", "customer")]]
            )
        return domain_quant_loc, domain_move_in_loc, domain_move_out_loc
