# -*- coding: utf-8 -*-
# (c) 2015 Daniel Campos - Avanzosc S.L.
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ProductSupplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    partner_code = fields.Char(related='name.ref')
