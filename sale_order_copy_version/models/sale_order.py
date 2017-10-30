# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, fields, models


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    version_number = fields.Integer(string="Version Number", copy=False,
                                    default=1)
    origin_name = fields.Char(string="Origin Number", copy=True)

    @api.model
    def create(self, vals):
        if 'name' in vals and not vals.get('origin_name', False):
            vals['origin_name'] = vals.get('name')
        return super(SaleOrder, self).create(vals)

    @api.multi
    def copy(self, default=None):
        if default is None:
            default = {}
        self.ensure_one()
        sales = self.search([('origin_name', '=ilike', self.origin_name)])
        last_version = max(sales.mapped('version_number'))
        default['origin_name'] = self.origin_name
        default['version_number'] = last_version + 1
        default['name'] = u'{}/{}'.format(self.origin_name,
                                          default['version_number'])
        return super(SaleOrder, self).copy(default=default)
