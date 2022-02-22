# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def unlink(self):
        if self.qty_delivered == 0.0 and self.product_id.type in ('product', 'consu'):
            self.unlink_related_stock_move()
            self.state = 'draft'
        elif self.qty_delivered > 0:
            raise UserError(
                _('You can not remove an order line once you have delivered!'))

        return super(SaleOrderLine, self).unlink()

    def unlink_related_stock_move(self):
        stock_moves = self.env['stock.move'].search([
            ('sale_line_id', '=', self.id)
        ])
        if len(stock_moves) == 1:
            if stock_moves.state not in ('cancel', 'done'):
                stock_moves.update({'state': 'draft'})
                stock_moves.unlink()

    # @api.onchange('product_uom_qty')
    # def _onchange_product_uom_qty(self):
    #     res = super(SaleOrderLine, self)._onchange_product_uom_qty()
    #     order_line = self._origin if self._origin else self
    #     for line in order_line:
    #         stock_move_lines = self.env['stock.move'].search([
    #             ('sale_line_id', '=', line.id)
    #         ])
    # 
    #         if len(stock_move_lines) == 1:
    #             stock_move_lines.update_stock_movement_qty_desc(
    #                 line.product_uom_qty, line.qty_delivered)
    #     return res
