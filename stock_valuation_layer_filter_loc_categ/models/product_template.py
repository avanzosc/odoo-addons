# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def write(self, vals):
        result = super(ProductTemplate, self).write(vals)
        if "categ_id" in vals:
            for template in self:
                template.change_categ_in_stock_valuation_layer_report()
        return result

    def change_categ_in_stock_valuation_layer_report(self):
        for product in self.product_variant_ids:
            cond = [("product_id", "=", product.id)]
            layers = self.env["stock.valuation.layer"].search(cond)
            if layers:
                vals = {
                    "product_categ_id": False,
                    "not_show_category_in_inventory_reports": False,
                }
                if self.categ_id:
                    show = product.categ_id.not_show_in_inventory_reports
                    vals = {
                        "product_categ_id": product.categ_id.id,
                        "not_show_category_in_inventory_reports": show,
                    }
                layers.write(vals)
