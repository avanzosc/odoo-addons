# Copyright 2024 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    location_qty_available = fields.Float(
        string="Quantity On Hand In Location",
        compute="_compute_location_quantities",
        compute_sudo=False,
        digits="Product Unit of Measure",
    )

    @api.depends_context("company", "location", "warehouse")
    def _compute_location_quantities(self):
        products = self.filtered(lambda p: p.type != "service")
        res = products.with_context(
            location_qty_available=True
        )._compute_quantities_dict(
            self._context.get("lot_id"),
            self._context.get("owner_id"),
            self._context.get("package_id"),
            self._context.get("from_date"),
            self._context.get("to_date"),
        )
        for product in products:
            product.location_qty_available = res[product.id]["qty_available"]

    def action_open_quants_real_stock(self):
        action = self.with_context(search_default_realstock=True).action_open_quants()
        return action

    def _get_domain_locations(self):
        (
            domain_quant_loc,
            domain_move_in_loc,
            domain_move_out_loc,
        ) = super()._get_domain_locations()
        if "location_qty_available" in self.env.context:
            domain_move_in_loc = [
                ("location_dest_id.real_stock_location", "=", True)
            ] + domain_move_in_loc
            domain_move_out_loc = [
                ("location_id.real_stock_location", "=", True)
            ] + domain_move_out_loc
            domain_quant_loc = [("real_stock_location", "=", True)] + domain_quant_loc
        return domain_quant_loc, domain_move_in_loc, domain_move_out_loc
