# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class StockLocation(models.Model):
    _inherit = "stock.location"

    location_id_computed = fields.Boolean(
        compute="compute_auxiliar", search="search_batch_type"
    )

    def compute_auxiliar(self):
        return True

    def search_batch_type(self, operator, value):
        batch_type = value
        if batch_type == "mother":
            reproductor = self.env.ref("stock_warehouse_farm.categ_type1")
            location_id_domain = [
                ("usage", "=", "internal"),
                ("type_id", "=", reproductor.id),
                ("activity", "=", "recry"),
            ]
        elif batch_type == "breeding":
            integration = self.env.ref("stock_warehouse_farm.categ_type2")
            location_id_domain = [
                ("usage", "=", "internal"),
                ("type_id", "=", integration.id),
            ]
        else:
            location_id_domain = []
        return location_id_domain
