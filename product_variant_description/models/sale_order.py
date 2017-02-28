# -*- coding: utf-8 -*-
# (c) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def product_id_change(
            self, pricelist, product, qty=0, uom=False, qty_uos=0, uos=False,
            name='', partner_id=False, lang=False, update_tax=True,
            date_order=False, packaging=False, fiscal_position=False,
            flag=False):
        res = super(SaleOrderLine, self).product_id_change(
            pricelist, product, qty=qty, uom=uom, qty_uos=qty_uos, uos=uos,
            name=name, partner_id=partner_id, lang=lang, update_tax=update_tax,
            date_order=date_order, packaging=packaging,
            fiscal_position=fiscal_position, flag=flag)
        if product:
            lang = self.env['res.partner'].browse(partner_id).lang
            product_o = self.env['product.product'].with_context(
                lang=lang).browse(product)
            if product_o.variant_description:
                res['value']['name'] = \
                    u'[{}] {}'.format(product_o.variant_description,
                                      res['value']['name'])
        return res
