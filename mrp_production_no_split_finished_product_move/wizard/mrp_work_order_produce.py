# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class MrpWorkOrderProduce(models.TransientModel):
    _inherit = 'mrp.work.order.produce'

    @api.multi
    def do_consume_produce(self):
        self.ensure_one()
        work_line = self.env['mrp.production.workcenter.line'].browse(
            self.env.context.get("active_id"))
        cond = [('production_id', '=', work_line.production_id.id)]
        procs = self.env['procurement.order'].search(cond, limit=1)
        if (not procs or
                procs.rule_id.procure_method != 'make_to_order'):
            move = work_line.production_id.move_created_ids.filtered(
                lambda x: x.product_id == work_line.production_id.product_id)
            if move and self.product_qty > move[0].product_uom_qty:
                move[0].write({'product_uom_qty': self.product_qty})
        return super(MrpWorkOrderProduce, self).do_consume_produce()
