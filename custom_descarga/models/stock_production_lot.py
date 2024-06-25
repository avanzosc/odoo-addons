# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockproductionLot(models.Model):
    _inherit = "stock.production.lot"

    def action_create_lot(self, product, name, company):
        lot = self.env["stock.production.lot"].create(
            {"name": name, "product_id": product.id, "company_id": company.id}
        )
        return lot
