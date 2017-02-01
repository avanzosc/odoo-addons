# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def _upgrade_sale_and_cost_price_from_wizard(self, sale_increase,
                                                 cost_increase):
        for product in self:
            vals = {}
            if sale_increase:
                vals['lst_price'] = product.lst_price * (1 + sale_increase)
            if cost_increase:
                vals['standard_price'] = (product.standard_price *
                                          (1 + cost_increase))
            product.write(vals)
