# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    possible_next_product_ids = fields.Many2many(
        comodel_name="product.product", compute="_next_product_ids")

    @api.multi
    def _get_next_products(self):
        self.ensure_one()
        product_obj = self.env['product.product']
        if not self.order_line:
            return product_obj.search([])
        restrict = self.order_line[:1].product_id.categ_id.category_restrict
        return product_obj.search(
            [('categ_id', '=', restrict.restricted_for.id)])

    @api.depends("order_line")
    def _next_product_ids(self):
            for order in self:
                self.possible_next_product_ids = [
                    (6, 0,  order._get_next_products()._ids)
            ]

    # @api.onchange("order_line")
    # def onchange_order_line(self):
    #     return {'domain': {'product_id': [('id', 'in',
    #                                        self._get_next_products()._ids)]}}


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _get_next_products(self):
        self.ensure_one()
        order = self.order_id
        product_obj = self.env['product.product']
        if not order.order_line[:1].product_id:
            return product_obj.search([])
        restrict = order.order_line[:1].product_id.categ_id.category_restrict
        return product_obj.search(
            [('categ_id', '=', restrict.restricted_for.id)])

    @api.onchange("product_id")
    def onchange_order_line(self):
        return {'domain': {'product_id': [('id', 'in',
                                           self._get_next_products()._ids)]}}