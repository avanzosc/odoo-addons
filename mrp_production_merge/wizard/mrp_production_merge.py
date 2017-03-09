# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import _, api, fields, models
from openerp.addons import decimal_precision as dp


class MrpProductionMerge(models.TransientModel):
    _name = 'mrp.production.merge'

    line_ids = fields.One2many(
        comodel_name='mrp.production.merge.line', inverse_name='merge_id')

    @api.model
    def default_get(self, fields_list):
        context = self.env.context
        res = super(MrpProductionMerge, self).default_get(fields_list)
        if context.get('active_model') == 'mrp.production' and\
                context.get('active_ids'):
            lines = []
            orders = self.env['mrp.production'].browse(context.get(
                'active_ids')).filtered(lambda p: p.state == 'draft')
            products = orders.mapped('product_id') if len(orders) > 1 else []
            for product in products:
                product_orders = orders.filtered(
                    lambda p: p.product_id == product)
                uoms = product_orders.mapped('product_uom') if len(
                    product_orders) > 1 else []
                for uom in uoms:
                    uom_orders = product_orders.filtered(
                        lambda p: p.product_uom == uom)
                    boms = uom_orders.mapped('bom_id') if len(
                        uom_orders) > 1 else []
                    for bom in boms:
                        bom_orders = uom_orders.filtered(
                            lambda p: p.bom_id == bom)
                        routings = bom_orders.mapped('routing_id') | \
                            bom_orders.mapped('bom_id.routing_id') if\
                            len(bom_orders) > 1 else []
                        for routing in routings:
                            line_orders = bom_orders.filtered(
                                lambda p: p.routing_id == routing or
                                (not p.routing_id and
                                 p.bom_id.routing_id == routing))
                            if len(line_orders) > 1:
                                lines.append([0, 0, {
                                    'product_id': product.id,
                                    'product_uom_id': uom.id,
                                    'bom_id': bom.id,
                                    'product_qty': sum(line_orders.mapped(
                                        'product_qty')),
                                    'date_planned': min(line_orders.mapped(
                                        'date_planned')),
                                    'routing_id': routing.id,
                                    'production_ids': [(6, 0,
                                                        line_orders.ids)],
                                }])
                        norouting_orders = bom_orders.filtered(
                            lambda p: not p.routing_id and not
                            p.bom_id.routing_id)
                        if norouting_orders and len(norouting_orders) > 1:
                            lines.append([0, 0, {
                                'product_id': product.id,
                                'product_uom_id': uom.id,
                                'bom_id': bom.id,
                                'product_qty': sum(norouting_orders.mapped(
                                    'product_qty')),
                                'date_planned': min(norouting_orders.mapped(
                                    'date_planned')),
                                'production_ids': [(6, 0,
                                                    norouting_orders.ids)],
                            }])
            res.update({'line_ids': lines})
        return res

    @api.multi
    def merge_manufacturing_orders_button(self):
        for line in self.line_ids:
            production = line.production_ids[:1]
            cancel_productions = line.production_ids[1:]
            production.write({
                'date_planned': line.date_planned,
                'product_qty': line.product_qty,
            })
            production.action_compute()
            for cancel_production in cancel_productions:
                cancel_production.message_post(
                    body=_(u'Manufacturing order merged in {}.'.format(
                        production.name)))
            cancel_productions.action_cancel()
        return True


class MrpProductionMergeLine(models.TransientModel):
    _name = 'mrp.production.merge.line'

    merge_id = fields.Many2one(
        comodel_name='mrp.production.merge', required=True)
    product_id = fields.Many2one(
        string='Product', comodel_name='product.product')
    product_qty = fields.Float(
        string='Product Quantity',
        digits=dp.get_precision('Product Unit of Measure'))
    product_uom_id = fields.Many2one(
        string='Product Unit of Measure', comodel_name='product.uom')
    bom_id = fields.Many2one(
        string='Bill of Material', comodel_name='mrp.bom')
    routing_id = fields.Many2one(
        string='Routing', comodel_name='mrp.routing')
    date_planned = fields.Datetime(
        string='Scheduled Date', required=True, select=1)
    production_ids = fields.Many2many(
        comodel_name='mrp.production', relation='mrp_production_merge_rel',
        column1='line_id', column2='production_id')
