# -*- coding: utf-8 -*-
# Copyright 2018 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import api, exceptions, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def product_id_change_with_wh(
            self, pricelist, product_id,
            qty=0, uom=False, qty_uos=0, uos=False, name='', partner_id=False,
            lang=False, update_tax=True, date_order=False, packaging=False,
            fiscal_position=False, flag=False, warehouse_id=False, context=None
    ):
        res = super(SaleOrderLine, self).product_id_change_with_wh(
            pricelist, product_id, qty, uom, qty_uos, uos, name,
            partner_id, lang, update_tax, date_order, packaging,
            fiscal_position, flag, warehouse_id, context=context)
        product = self.env['product.product'].browse(product_id)
        if product.price_valid_date < fields.Datetime.now():
            res['warning'] = {
                'title': _('Warning'),
                'message': _('The valid price date has expired: {}'.format(
                    product.name))}
        return res


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.multi
    def action_button_confirm(self):
        for record in self:
            price_valid_dates = record.order_line.filtered(
                lambda x: x.product_id.price_valid_date < fields.Datetime.now()
            )
            if price_valid_dates:
                raise exceptions.ValidationError(
                    _("At least one product has expired valid date "
                      "price: {}".format(
                        price_valid_dates.mapped("product_id.name"))))
        return super(SaleOrder, self).action_button_confirm()
