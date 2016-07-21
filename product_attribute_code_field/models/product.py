# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class ProductAttribute(models.Model):

    _inherit = 'product.attribute'

    attribute_code = fields.Char(string='Code', required=True)

    @api.constrains('attribute_code')
    def _code_unique(self):
        if len(self.search([('attribute_code', '=', self.attribute_code)])) \
                > 1:
            raise exceptions.ValidationError(
                _("Code already exists and violates unique field constraint"))
