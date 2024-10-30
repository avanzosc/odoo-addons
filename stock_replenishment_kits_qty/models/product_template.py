import logging

from odoo import models

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _compute_qty_in_kits(self):
        product_product_model = self.env["product.product"]
        product_product_model._compute_qty_in_kits()
