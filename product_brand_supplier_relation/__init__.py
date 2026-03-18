from . import models
from odoo import api, SUPERUSER_ID


def _post_install_load_data_into_relational_table(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    cond = [("partner_id", "!=", False), ("product_brand_id", "!=", False)]
    supplierinfos = env["product.supplierinfo"].search(cond)
    for supplierinfo in supplierinfos:
        supplierinfo._search_product_brand_supplier_rel()
