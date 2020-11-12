# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class StockPickingDuplicate(models.TransientModel):
    _name = 'stock.picking.duplicate'
    _description = 'Stock Picking Duplicate'

    scheduled_date = fields.Datetime('Scheduled Date', required=True)

    @api.multi
    def duplicate_picking(self):
        picking_obj = self.env['stock.picking']
        picking_lst = []
        date_code = '{}{}{}'.format(self.scheduled_date.year,
                                    self.scheduled_date.month,
                                    self.scheduled_date.day)
        for picking in picking_obj.search(
                [('id', 'in', self.env.context['active_ids'])]):
            pk = picking.copy({'scheduled_date': self.scheduled_date,
                               'is_template': False})
            picking_lst.append(pk.id)
            pk.action_confirm()
            for move in pk.move_lines:
                if move.product_id.tracking == 'serial':
                    i = 1
                    for move_line in move.move_line_ids:
                        move_line.lot_name = '{}.{}-{}'.format(
                            i, date_code, picking.partner_id.name)
                        i += 1
        if picking_lst:
            action = self.env.ref('stock.action_picking_tree_all')
            action_dict = action.read()[0] if action else {}
            domain = expression.AND([
                [('id', 'in', picking_lst)], safe_eval(action.domain or '[]')])
            action_dict.update({'domain': domain})
            return action_dict
        return {'type': 'ir.actions.act_window_close'}
