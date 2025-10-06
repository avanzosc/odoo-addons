from odoo import api, models


class StockInventoryLine(models.Model):
    _inherit = "stock.inventory.line"

    @api.model
    def read_group(
        self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True
    ):
        res = super().read_group(
            domain,
            fields,
            groupby,
            offset=offset,
            limit=limit,
            orderby=orderby,
            lazy=lazy,
        )
        if "difference_qty" in fields:
            for r in res:
                if "__domain" in r:
                    lines = self.search(r["__domain"])
                    r["difference_qty"] = sum(
                        line.product_qty - line.theoretical_qty for line in lines
                    )
        return res
