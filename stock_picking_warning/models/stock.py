# -*- coding: utf-8 -*-
# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def do_enter_transfer_details(self):
        for picking in self:
            moves = False
            if picking.picking_type_id.code == 'outgoing':
                moves = picking.mapped('move_lines').filtered(
                    lambda l: l.product_id and
                    l.product_id.out_picking_warn == 'block')
            if picking.picking_type_id.code == 'incoming':
                moves = picking.mapped('move_lines').filtered(
                    lambda l: l.product_id and
                    l.product_id.in_picking_warn == 'block')
            if moves:
                err = ''
                for move in moves:
                    err += u"{}{}{}: {}\n".format(
                        err, _('Product '), move.product_id.name,
                        move.product_id.out_picking_warn_msg
                        if picking.picking_type_id.code == 'outgoing' else
                        move.product_id.in_picking_warn_msg)
                raise exceptions.Warning(err)
        return super(StockPicking, self).do_enter_transfer_details()


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.multi
    def onchange_product_id(self, prod_id=False, loc_id=False,
                            loc_dest_id=False, partner_id=False):
        res = super(StockMove, self).onchange_product_id(
            prod_id=prod_id, loc_id=loc_id, loc_dest_id=loc_dest_id,
            partner_id=partner_id)
        if prod_id and self.env.context.get('default_picking_type_id', False):
            prod = self.env['product.product'].browse(prod_id)
            type = self.env['stock.picking.type'].browse(
                self.env.context.get('default_picking_type_id'))
            if prod.out_picking_warn == 'warning' and type.code == 'outgoing':
                warning = {'title': _('Product out picking warning'),
                           'message': prod.out_picking_warn_msg}
                res['warning'] = warning
            if prod.in_picking_warn == 'warning' and type.code == 'incoming':
                warning = {'title': _('Product in picking warning'),
                           'message': prod.in_picking_warn_msg}
                res['warning'] = warning
        return res
