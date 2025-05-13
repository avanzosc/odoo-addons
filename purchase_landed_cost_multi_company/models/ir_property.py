# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models


class IrProperty(models.Model):
    _inherit = "ir.property"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if ("name" in vals and vals.get("name") == "standard_price"and
                    "res_id" in vals and "product.product" in vals.get("res_id")):
                product = self._get_product_from_values(vals.get("res_id"))
                if product.company_id:
                    vals["company_id"] = product.company_id.id
        return super(IrProperty, self).create(vals_list)

    @api.multi
    def write(self, values):
        if (len(self) == 1 and self.name == "standard_price" and
                "product.product" in self.res_id):
            product = self._get_product_from_values(self.res_id)
            if product.company_id and product.company_id != self.company_id:
                my_res_id = "product.product,%(product_id)s" % {"product_id": product.id,}
                cond = [("res_id", "=", my_res_id),
                        ("name", "=", "standard_price"),
                        ("company_id", "=", product.company_id.id)]
                my_property = self.env["ir.property"].search(cond, limit=1)
                if my_property:
                    return super(IrProperty, my_property).write(values)
        return super(IrProperty, self).write(values)

    def _get_product_from_values(self, res_id):
        return self.env["product.product"].browse(int(res_id.split(",")[1]))
