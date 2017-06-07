# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ProductUl(models.Model):

    _inherit = 'product.ul'

    qty = fields.Float(string='Package Qty', default=1)
