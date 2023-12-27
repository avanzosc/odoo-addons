# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def create(self, vals):
        picking_obj = self.env['stock.picking']
        if (not vals.get("partner_id", False) and
                vals.get("picking_id", False)):
            picking = picking_obj.browse(vals.get('picking_id'))
            vals['partner_id'] = picking.partner_id.id
        move = super(StockMove, self).create(vals)
        return move
