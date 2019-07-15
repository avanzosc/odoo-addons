# -*- coding: utf-8 -*-
# Copyright 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields, _


class ProductProduct(models.Model):
    _inherit = 'product.product'

    unique = fields.Boolean(string='Unique', default=True)

    @api.multi
    def set_as_deactivated_from_picking(self, picking):
        self.active = False
        body = u"<p>{}: {}/{} {}: {} {}: {}</p>".format(
            _('Sold Product'), self.default_code, self.name, _('to'),
            picking.partner_id.name, _('in picking'), picking.name)
        self.message_post(body=body, type='comment')
        if len(self.product_tmpl_id.product_variant_ids.filtered(
               lambda x: x.active)) == 0 and self.product_tmpl_id.active:
            self.product_tmpl_id.active = False

    @api.multi
    def set_as_activated_from_picking(self, picking):
        self.active = True
        body = u"<p>{}: {}/{} {}: {} {}: {}</p>".format(
            _('Product return'), self.default_code, self.name, _('by'),
            picking.partner_id.name, _('from picking'), picking.name)
        self.message_post(body=body, type='comment')
        if not self.product_tmpl_id.active:
            self.product_tmpl_id.active = True
