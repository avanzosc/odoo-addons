# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProductProduct(models.Model):
    _inherit = "product.product"

    @api.multi
    def _get_domain_dates(self):
        if not self.env.context.get('to_date_expected'):
            return super(ProductProduct, self)._get_domain_dates()
        domain = [('date_expected_without_hour', '<=',
                   self.env.context.get('to_date_expected'))]
        return domain
