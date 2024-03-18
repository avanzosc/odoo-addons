# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom,
                               location_id, name, origin, values, group_id):
        values = super(StockRule, self)._get_stock_move_values(
            product_id, product_qty, product_uom, location_id, name, origin,
            values, group_id)
        if group_id:
            group = self.env['procurement.group'].browse(group_id)
            if (group and group.sale_id and group.sale_id.type_id and
                    group.sale_id.type_id.picking_type_id):
                values['picking_type_id'] = (
                    group.sale_id.type_id.picking_type_id.id)
        return values
