from odoo import fields, models
from odoo.osv import expression


class StockInventory(models.Model):
    _inherit = "stock.inventory"

    create_date_before = fields.Datetime()
    lot_contains = fields.Char()

    def _get_inventory_quant_filter_domain(self):
        self.ensure_one()
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
        ]
        return domain

    def _add_inventory_quant_filter_domain(self, domain):
        self.ensure_one()
        quant_filter_domain = self._get_inventory_quant_filter_domain()
        if not quant_filter_domain:
            return domain
        return expression.AND([domain, quant_filter_domain])

    def _get_domain_all_quants(self, base_domain):
        domain = super()._get_domain_all_quants(base_domain)
        return self._add_inventory_quant_filter_domain(domain)

    def _get_domain_manual_quants(self, base_domain):
        domain = super()._get_domain_manual_quants(base_domain)
        return self._add_inventory_quant_filter_domain(domain)

    def _get_domain_one_quant(self, base_domain):
        domain = super()._get_domain_one_quant(base_domain)
        return self._add_inventory_quant_filter_domain(domain)

    def _get_domain_lot_quants(self, base_domain):
        domain = super()._get_domain_lot_quants(base_domain)
        return self._add_inventory_quant_filter_domain(domain)

    def _get_domain_category_quants(self, base_domain):
        domain = super()._get_domain_category_quants(base_domain)
        return self._add_inventory_quant_filter_domain(domain)
