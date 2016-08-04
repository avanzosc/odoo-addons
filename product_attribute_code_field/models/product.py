# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, exceptions, _


class ProductAttribute(models.Model):

    _inherit = 'product.attribute'

    @api.onchange('name')
    def onchange_name(self):
        for product in self:
            if product.name:
                product.attribute_code = product.name[0:2]

    attribute_code = fields.Char(string='Code', default=onchange_name,
                                 required=True)

    @api.constrains('attribute_code')
    def _code_unique(self):
        if len(self.search([('attribute_code', '=', self.attribute_code)])) \
                > 1:
            raise exceptions.ValidationError(
                _("Code already exists and violates unique field constraint"))
