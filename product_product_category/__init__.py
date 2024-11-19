from . import models

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)


def post_init_hook(cr, registry):
    _logger.info("Starting product_product_category post_init_hook execution.")

    env = api.Environment(cr, SUPERUSER_ID, {})

    products = env["product.product"].search([])

    _logger.info("Found %d products with product_tmpl_id.", len(products))

    for product in products:
        try:
            product.product_category = product.product_tmpl_id.categ_id
            _logger.info(
                "Updated product %s with category %s",
                product.name,
                product.product_category.name,
            )
        except Exception as e:
            _logger.error("Error updating product %s: %s", product.name, str(e))

    _logger.info("Finished post_init_hook execution.")
