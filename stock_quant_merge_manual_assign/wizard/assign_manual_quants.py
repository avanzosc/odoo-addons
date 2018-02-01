# -*- coding: utf-8 -*-
# Copyright 2018 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models


class AssignManualQuants(models.TransientModel):

    _inherit = 'assign.manual.quants'

    @api.multi
    def assign_quants(self):
        quant_model = self.env['stock.quant']
        move = self.env['stock.move'].browse(self.env.context['active_id'])
        move.picking_id.mapped('pack_operation_ids').unlink()
        quant_merge_dict = {}
        for quant in move.reserved_quant_ids:
            quants = quant_model.search(quant._mergeable_domain())
            quants |= quant
            quant_merge_dict[quant.id] = sum(self.quants_lines.filtered(
                lambda x: x.quant.id in quants.ids).mapped('qty'))
        quants = []
        move.do_unreserve()
        for line in self.quants_lines:
            if line.selected:
                qty = line.qty
                if line.quant.id in quant_merge_dict:
                    qty = quant_merge_dict[line.quant.id]
                quants.append([line.quant, qty])
        self.pool['stock.quant'].quants_reserve(
            self.env.cr, self.env.uid, quants, move, context=self.env.context)
        return {}
