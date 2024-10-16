# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def write(self, vals):
        result = super(ProductProduct, self).write(vals)
        if "categ_id" in vals:
            for product in self:
                product.change_categ_in_stock_valuation_layer_report()
        return result

    def change_categ_in_stock_valuation_layer_report(self):
        cond = [("product_id", "=", self.id)]
        layers = self.env["stock.valuation.layer"].search(cond)
        if layers:
            vals = {
                "product_categ_id": False,
                "not_show_category_in_inventory_reports": False,
            }
            if self.categ_id:
                show = self.categ_id.not_show_in_inventory_reports
                vals = {
                    "product_categ_id": self.categ_id.id,
                    "not_show_category_in_inventory_reports": show,
                }
            layers.write(vals)
