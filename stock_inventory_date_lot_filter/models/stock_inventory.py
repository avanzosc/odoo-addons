from collections import OrderedDict

from odoo import fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    create_date_before = fields.Datetime(string="Create Date Before")
    lot_contains = fields.Char(string="Lot Contains")

    def _get_inventory_lines_values(self):
        self.ensure_one()
        quants_groups = self._get_quantities()
        vals = []
        product_ids = OrderedDict()
        StockQuant = self.env["stock.quant"]
        StockLot = self.env["stock.production.lot"]

        for (
            product_id,
            location_id,
            lot_id,
            package_id,
            owner_id,
        ), quantity in quants_groups.items():
            domain = [
                ("product_id", "=", product_id),
                ("location_id", "=", location_id),
                ("lot_id", "=", lot_id),
                ("package_id", "=", package_id),
                ("owner_id", "=", owner_id),
            ]
            quant = StockQuant.search(domain, limit=1)

            if (
                self.create_date_before
                and quant.create_date
                and quant.create_date >= self.create_date_before
            ):
                continue

            if self.lot_contains and lot_id:
                lot = StockLot.browse(lot_id)
                if lot and self.lot_contains.lower() not in lot.name.lower():
                    continue

            line_values = {
                "inventory_id": self.id,
                "product_qty": 0
                if self.prefill_counted_quantity == "zero"
                else quantity,
                "theoretical_qty": quantity,
                "prod_lot_id": lot_id,
                "partner_id": owner_id,
                "product_id": product_id,
                "location_id": location_id,
                "package_id": package_id,
            }
            product_ids[product_id] = None
            vals.append(line_values)

        product_browse = self.env["product.product"].browse(list(product_ids.keys()))
        for product in product_browse:
            product_ids[product.id] = product

        for val in vals:
            product = product_ids[val["product_id"]]
            val["product_uom_id"] = product.product_tmpl_id.uom_id.id

        if self.exhausted:
            vals += self._get_exhausted_inventory_lines_vals(
                {(line["product_id"], line["location_id"]) for line in vals}
            )

        return vals
