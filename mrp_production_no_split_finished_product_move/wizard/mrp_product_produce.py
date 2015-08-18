# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

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
                if procs:
                    production = self.env['mrp.production'].browse(
                        production_id)
                    move = production.move_created_ids.filtered(
                        lambda x: x.product_id == production.product_id)
                    if move and self.product_qty > move[0].product_uom_qty:
                        move[0].write({'product_uom_qty': self.product_qty})
        return super(MrpProductProduce, self).do_produce()
