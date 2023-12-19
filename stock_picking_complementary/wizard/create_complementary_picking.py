# Copyright 2020 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class CreateComplementaryPicking(models.TransientModel):
    _name = "create.complementary.picking"
    _rec_name = "location_id"

    location_id = fields.Many2one(comodel_name="stock.location")

    @api.multi
    def create_complementary(self):
        self.ensure_one()
        check_pickings = self.env['stock.picking'].search(
            [('id', 'in', self._context.get('active_ids')),
             ('show_check_availability', '=', True)])
        check_pickings.action_assign()
        pickings = check_pickings.filtered(lambda x: x.show_check_availability)
        res = pickings.create_complementary_picking(self.location_id)
        if len(res) == 1:
            return {
                'view_mode': 'form',
                'view_type': 'form',
                'res_model': 'stock.picking',
                'res_id': res[0][1].id,
                'type': 'ir.actions.act_window',
            }
