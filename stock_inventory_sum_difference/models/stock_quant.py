from odoo import api, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    @api.model
    @api.readonly
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
        if "inventory_diff_quantity" in fields:
            for group in res:
                if "__domain" in group:
                    quants = self.search(group["__domain"])
                    group["inventory_diff_quantity"] = sum(
                        quants.mapped("inventory_diff_quantity")
                    )
        return res
