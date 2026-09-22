# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCatalog(models.Model):
    _inherit = "product.catalog"

    visible_slider = fields.Boolean(string="Visible on Website", default=True)

    def _get_product_tmpl_ids(self):
        if not self.ids:
            return []
        self.env.cr.execute(
            """
            SELECT DISTINCT COALESCE(pli.product_tmpl_id, pp.product_tmpl_id)
              FROM pricelist_item_catalog_rel rel
              JOIN product_pricelist_item pli ON pli.id = rel.pricelist_item_id
              LEFT JOIN product_product pp ON pp.id = pli.product_id
             WHERE rel.catalog_id = ANY(%s)
               AND COALESCE(pli.product_tmpl_id, pp.product_tmpl_id) IS NOT NULL
            """,
            [self.ids],
        )
        return [row[0] for row in self.env.cr.fetchall()]
