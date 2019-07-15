# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    prices = fields.Char(string='Prices', compute='_compute_prices')
    #  This field will work if it is not defined as store true if supplierinfo
    #  for customer is installed

    @api.depends('pricelist_ids', 'pricelist_ids.price',
                 'pricelist_ids.min_quantity')
    def _compute_prices(self):
        for record in self:
            data = []
            info = record.pricelist_ids._fields
            qty_digits = info['min_quantity'].digits and\
                info['min_quantity'].digits[1] or 2
            price_digits =\
                info['price'].digits and info['price'].digits[1] or 2
            base = "[{{:.{:d}f}}] {{:.{:d}f}}".format(qty_digits, price_digits)
            for partnerinfo in record.pricelist_ids.sorted(
                    lambda r: r.min_quantity):
                data.append(base.format(partnerinfo.min_quantity,
                                        partnerinfo.price))
            record.prices = ' // '.join(data)
