# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class ProductCatalog(models.Model):
    _name = "product.catalog"
    _inherit = [
        "rating.mixin",
        "product.catalog",
        "website.seo.metadata",
        "website.published.multi.mixin",
        "website.searchable.mixin",
    ]

    def _get_product_tmpl_ids(self):
        if not self.ids:
            return []
        self.env.cr.execute(
            """
            WITH valid_items AS (
                SELECT
                    pli.id,
                    pli.applied_on,
                    pli.product_id,
                    pli.product_tmpl_id,
                    pli.categ_id
                FROM pricelist_item_catalog_rel rel
                JOIN product_pricelist_item pli ON pli.id = rel.pricelist_item_id
                WHERE rel.catalog_id = ANY(%s)
                  AND (pli.date_start IS NULL OR pli.date_start <= NOW())
                  AND (pli.date_end IS NULL OR pli.date_end >= NOW())
            ),
            tmpl_from_variant AS (
                SELECT DISTINCT pp.product_tmpl_id AS id
                FROM valid_items vi
                JOIN product_product pp ON pp.id = vi.product_id
                JOIN product_template pt ON pt.id = pp.product_tmpl_id
                WHERE vi.applied_on = '0_product_variant'
                  AND COALESCE(pp.active, TRUE)
                  AND COALESCE(pt.active, TRUE)
            ),
            tmpl_from_product AS (
                SELECT DISTINCT vi.product_tmpl_id AS id
                FROM valid_items vi
                JOIN product_template pt ON pt.id = vi.product_tmpl_id
                WHERE vi.applied_on = '1_product'
                  AND vi.product_tmpl_id IS NOT NULL
                  AND COALESCE(pt.active, TRUE)
            ),
            tmpl_from_categ AS (
                SELECT DISTINCT pt.id
                FROM valid_items vi
                JOIN product_category pc ON pc.id = vi.categ_id
                JOIN product_template pt ON pt.categ_id IN (
                    SELECT id
                    FROM product_category
                    WHERE parent_path LIKE pc.parent_path || '%%'
                )
                WHERE vi.applied_on = '2_product_category'
                  AND vi.categ_id IS NOT NULL
                  AND COALESCE(pt.active, TRUE)
            ),
            tmpl_from_global AS (
                SELECT DISTINCT pt.id
                FROM valid_items vi
                CROSS JOIN product_template pt
                WHERE vi.applied_on = '3_global'
                  AND COALESCE(pt.active, TRUE)
            )
            SELECT DISTINCT id
            FROM (
                SELECT id FROM tmpl_from_variant
                UNION ALL
                SELECT id FROM tmpl_from_product
                UNION ALL
                SELECT id FROM tmpl_from_categ
                UNION ALL
                SELECT id FROM tmpl_from_global
            ) t
            WHERE id IS NOT NULL
            """,
            [self.ids],
        )
        return [row[0] for row in self.env.cr.fetchall()]

    def _compute_website_url(self):
        result = super()._compute_website_url()
        for catalog in self:
            if catalog.id:
                catalog.website_url = "/catalog/{}".format(
                    self.env["ir.http"]._slug(catalog)
                )
        return result

    def _catalog_get_portal_domain(self):
        if self.env.user.has_group("base.group_user"):
            # Then, he is internal user, and we take the domain for this current user
            return self.env["ir.rule"]._compute_domain(self._name)
        return [
            ("is_published", "=", True),
        ]
