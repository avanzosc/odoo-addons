# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    vat_price = fields.Float(string='VAT price', compute='_compute_vat_price')

    @api.depends("list_price", "taxes_id")
    def _compute_vat_price(self):
        for product in self:
            if product.list_price:
                product.vat_price = product.list_price
                for taxes in product.taxes_id:
                    vat = product.list_price * taxes.amount / 100
                    product.vat_price += vat
