# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    env.cr.execute(
        "update product_pricelist_item "
        "set product_default_code = (select p.default_code "
        "                            from product_product p "
        "                            where p.id = product_pricelist_item.product_id) "
        "where product_tmpl_id is null "
        "  and product_id is not null;"
    )

    env.cr.execute(
        "update product_pricelist_item "
        "set product_default_code = (select t.default_code "
        "                            from product_template t "
        "                            where t.id = product_pricelist_item.product_tmpl_id) "
        "where product_tmpl_id is not null "
        "  and product_id is null;"
    )
