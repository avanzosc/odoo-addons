##############################################################################
#
# Copyright 2019 Odoo IT now <http://www.odooitnow.com/>
# See LICENSE file for full copyright and licensing details.
#
##############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    location_id = fields.Many2one('stock.location', string="Location",
                                  domain="[('usage','=','internal')]")
    sale_type_id = fields.Many2one(
        comodel_name='sale.order.type', string='Sale type')

    @api.onchange('sale_type_id')
    def _onchange_sale_type_id(self):
        for line in self:
            line.location_id = False
            if line.sale_type_id and line.sale_type_id.location_id:
                line.location_id = line.sale_type_id.location_id.id

    @api.onchange('product_uom_qty', 'product_uom', 'route_id', 'location_id')
    def _onchange_product_id_check_availability(self):
        warehouse_obj = self.env['stock.warehouse']
        if (not self.product_id or not self.product_uom_qty or not
                self.product_uom):
            self.product_packaging = False
            return {}
        if not self.location_id:
            return super(SaleOrderLine,
                         self)._onchange_product_id_check_availability()
        if self.product_id.type == 'product':
            precision = self.env['decimal.precision'].precision_get(
                'Product Unit of Measure')
            product = self.product_id.with_context(
                warehouse=self.order_id.warehouse_id.id,
                location=self.location_id.id,
                lang=(self.order_id.partner_id.lang or self.env.user.lang or
                      'en_US')
            )
            product_qty = self.product_uom._compute_quantity(
                self.product_uom_qty, self.product_id.uom_id)
            if float_compare(product.virtual_available, product_qty,
                             precision_digits=precision) == -1:
                is_available = self._check_routing()
                if not is_available:
                    message = _(
                        'You plan to sell %s %s of %s but you only have %s %s'
                        ' available in location %s.') % (
                            self.product_uom_qty, self.product_uom.name,
                            self.product_id.name, product.virtual_available,
                            product.uom_id.name, self.location_id.name)
                    if float_compare(product.virtual_available,
                                     self.product_id.virtual_available,
                                     precision_digits=precision) == -1:
                        message += _('\nThere are %s %s available across all'
                                     ' warehouses.\n\n') % \
                                     (self.product_id.virtual_available,
                                      product.uom_id.name)
                        for warehouse in warehouse_obj.search([]):
                            quantity = self.product_id.with_context(
                                warehouse=warehouse.id).virtual_available
                            if quantity > 0:
                                message += "%s: %s %s\n" % (
                                    warehouse.name, quantity,
                                    self.product_id.uom_id.name)
                    warning_mess = {
                        'title': _('Not enough inventory!'),
                        'message': message
                    }
                    return {'warning': warning_mess}
        return {}


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('order_line')
    def _check_product_location(self):
        for order in self:
            for line in order.order_line.filtered(
                    lambda l: l.location_id and l.sale_type_id and
                    l.product_id):
                lines_count = line.search_count(
                    [('order_id', '=', order.id),
                     ('product_id', '=', line.product_id.id),
                     ('location_id', '=', line.location_id.id),
                     ('sale_type_id', '=', line.sale_type_id.id)])
                if lines_count > 1:
                    raise ValidationError(
                        _("""You cannot add same product %s with
                            the same location %s and sale type %s.""" % (
                                line.product_id.display_name,
                                line.location_id.display_name,
                                line.sale_type_id.name)))


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(
            self, product_id, product_qty, product_uom, location_id,
            name, origin, values, group_id):
        if values.get('sale_line_id', False):
            sale_line_id = self.env['sale.order.line'].sudo().browse(
                values['sale_line_id'])
            if sale_line_id.location_id:
                self.location_src_id = sale_line_id.location_id.id
            else:
                self.location_src_id = (
                    self.picking_type_id.default_location_src_id.id)
        result = super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id,
            name, origin, values, group_id)
        if values.get('sale_line_id', False) and sale_line_id.sale_type_id:
            result['picking_type_id'] = (
                sale_line_id.sale_type_id.picking_type_id.id)
        return result


class SaleOrderType(models.Model):
    _inherit = 'sale.order.type'
    _order = 'sequence'

    sequence = fields.Integer(
        string='Sequence', default=1)
    location_id = fields.Many2one(
        string='Location', comodel_name='stock.location')
