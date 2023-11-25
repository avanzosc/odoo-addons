# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductCategory(models.Model):
    _inherit = "product.category"

    def write(self, vals):
        result = super(ProductCategory, self).write(vals)
        if "not_show_in_inventory_reports" in vals:
            for category in self:
                category.put_show_in_stock_valuation_layer_report()
        return result

    def put_show_in_stock_valuation_layer_report(self):
        cond = [("product_categ_id", "=", self.id)]
        layers = self.env["stock.valuation.layer"].search(cond)
        if layers:
            layers.write(
                {"not_show_category_in_inventory_reports":
                 self.not_show_in_inventory_reports}
                )
