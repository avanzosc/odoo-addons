# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    global_origin_initial = fields.Boolean(
        string="Initial",
        copy=False,
        tracking=True,
        help="Start of a chain to track: every purchase, manufacturing order and "
        "stock move that serves this order, in any company, gets its name as "
        "Global Origin.",
    )
    global_origin = fields.Char(
        compute="_compute_global_origin", store=True, index=True, recursive=True
    )

    @api.depends(
        "name", "global_origin_initial", "auto_purchase_order_id.global_origin"
    )
    def _compute_global_origin(self):
        for order in self:
            order.global_origin = order.auto_purchase_order_id.global_origin or (
                order.name if order.global_origin_initial else False
            )

    def _recompute_global_origin(self):
        origins = [
            origin
            for origin in set(self.mapped("name") + self.mapped("global_origin"))
            if origin
        ]
        # Before marking anything: Odoo does not spread the recomputation through
        # records that are already marked to compute
        self.sudo().modified(["global_origin_initial"])
        for model_name in (
            "sale.order",
            "purchase.order",
            "mrp.production",
            "stock.move",
        ):
            model = self.env[model_name].sudo()
            self.env.add_to_compute(
                model._fields["global_origin"],
                model.search([("global_origin", "in", origins)]),
            )
        self.env.flush_all()
