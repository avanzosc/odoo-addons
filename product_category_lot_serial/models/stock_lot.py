# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class StockLot(models.Model):
    _inherit = "stock.lot"

    name = fields.Char(default="/")

    @api.model_create_multi
    def create(self, vals_list):
        self._check_create()
        for vals in vals_list:
            if "lot_by_category" in self.env.context:
                del vals["name"]
            if (
                "product_id" in vals
                and vals.get("product_id", False)
                and (
                    "name" not in vals
                    or not vals.get("name")
                    or vals.get("name") == "/"
                )
            ):
                product = self.env["product.product"].browse(vals.get("product_id"))
                if product.categ_id and product.categ_id.sequence_id:
                    vals["name"] = product.categ_id.sequence_id.next_by_id()
                else:
                    vals["name"] = self.env.ref(
                        "stock.sequence_production_lots"
                    ).next_by_id()
        a = super().create(vals_list)
        return a
