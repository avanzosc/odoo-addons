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
        pickings = self.env['stock.picking'].browse(self._context.get(
            'active_ids'))
        picking = pickings.create_complementary_picking(self.location_id)
        return {
            'view_mode': 'form',
            'view_type': 'form',
            'res_model': 'stock.picking',
            'res_id': picking.id,
            'type': 'ir.actions.act_window',
        }
