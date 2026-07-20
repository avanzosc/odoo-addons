# Copyright 2022 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_out_svl_vals(self, quantity, company, lot=False):
        """Prepare the values for a stock valuation layer created by a delivery.

        :param quantity: the quantity to value, expressed in `self.uom_id`
        :return: values to use in a call to create
        :rtype: dict
        """
        product = self.with_company(company)
        vals = super(ProductProduct, product)._prepare_out_svl_vals(
            quantity, company, lot=lot
        )
        vals.update(
            {
                "valuation": product.valuation,
                "cost_method": product.cost_method,
            }
        )
        return vals
