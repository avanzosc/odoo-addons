# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    @api.multi
    def do_produce(self):
        self.ensure_one()
        if self.mode == 'consume_produce':
            production_id = self.env.context.get('active_id', False)
            if production_id:
                cond = [('production_id', '=', production_id)]
                procs = self.env['procurement.order'].search(cond, limit=1)
                if (not procs or
                        procs.rule_id.procure_method != 'make_to_order'):
                    production = self.env['mrp.production'].browse(
                        production_id)
                    move = production.move_created_ids.filtered(
                        lambda x: x.product_id == self.product_id)
                    if move and self.product_qty > move[0].product_uom_qty:
                        move[0].write({'product_uom_qty': self.product_qty})
        return super(MrpProductProduce, self).do_produce()
