# Copyright (c) 2018 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, exceptions, fields, models, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    no_discount_price = fields.Float('Real price',
                                     compute='_compute_real_price')

    def _compute_real_price(self):
        for order in self:
            amount = 0
            for line in order.order_line:
                amount = amount + \
                    line.product_id.lst_price * line.product_uom_qty
            order.no_discount_price = amount

    def check_actual_credit(self, partner_id):
        move_obj = self.env['stock.move']
        location_obj = self.env['stock.location']
        internal_ids = location_obj.search([('usage', '=', 'internal')]).ids
        negative_moves = move_obj.search([
            ('partner_id', '=', partner_id),
            ('location_id', 'in', internal_ids),
            ('location_dest_id', 'not in', internal_ids)])
        negative_amount = sum([x.product_price for x in negative_moves])
        positive_moves = move_obj.search([
            ('partner_id', '=', partner_id),
            ('location_id', 'not in', internal_ids),
            ('location_dest_id', 'in', internal_ids)])
        positive_amount = sum([x.product_price for x in positive_moves])
        return negative_amount - positive_amount

    @api.multi
    def action_confirm(self):
        for order in self:
            if order.partner_id.property_product_pricelist.has_limit:
                actual_credit = self.check_actual_credit(order.partner_id.id)
                limit = (
                    order.partner_id.property_product_pricelist.limit_amount -
                    (order.no_discount_price + actual_credit))
                if limit < 0:
                    raise exceptions.Warning(
                        _(u'Sale amount exceeded pricelist limit by: {}'.
                          format(abs(limit))))
        return super(SaleOrder, self).action_confirm()
