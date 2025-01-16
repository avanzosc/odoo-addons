# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    def name_get(self):
        result = []
        for supplierinfo in self:
            product_name = (
                supplierinfo.product_name
                if supplierinfo.product_name
                else supplierinfo.partner_id.name
            )
            if supplierinfo.product_code:
                name = "[{}] {}".format(supplierinfo.product_code, product_name)
            else:
                name = "{}".format(product_name)
            result.append((supplierinfo.id, name))
        return result
