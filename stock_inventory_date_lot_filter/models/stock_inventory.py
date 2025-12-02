from odoo import fields, models


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    create_date_before = fields.Datetime(string="Create Date Before")
    lot_contains = fields.Char(string="Lot Contains")

    def _get_inventory_lines_values(self):
        self.ensure_one()
        StockQuant = self.env["stock.quant"]
        domain = [
            ("quantity", "!=", 0),
            *(
                [("create_date", "<", self.create_date_before)]
                if self.create_date_before
                else []
            ),
            *(
                [("lot_id.name", "ilike", self.lot_contains)]
                if self.lot_contains
                else []
            ),
            *(
                [("location_id", "in", self.location_ids.ids)]
                if self.location_ids
                else []
            ),
            *([("product_id", "in", self.product_ids.ids)] if self.product_ids else []),
        ]
        quants = StockQuant.search(domain)
        vals = []
        for quant in quants:
            vals.append(
                {
                    "inventory_id": self.id,
                    "product_id": quant.product_id.id,
                    "location_id": quant.location_id.id,
                    "prod_lot_id": quant.lot_id.id,
                    "package_id": quant.package_id.id,
                    "partner_id": quant.owner_id.id,
                    "theoretical_qty": quant.quantity,
                    "product_qty": 0
                    if self.prefill_counted_quantity == "zero"
                    else quant.quantity,
                    "product_uom_id": quant.product_id.uom_id.id,
                }
            )
        if self.exhausted:
            vals += self._get_exhausted_inventory_lines_vals(
                {(line["product_id"], line["location_id"]) for line in vals}
            )
        return vals
