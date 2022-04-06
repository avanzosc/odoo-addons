# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    def _refresh_quants_by_picking_cancelation(self):
        quant_obj = self.env['stock.quant']
        cond = self._quant_condition_for_picking_cancelation(
            self.location_dest_id)
        quant = quant_obj.search(cond)
        quant.sudo().quantity = quant.quantity - self.qty_done
        cond = self._quant_condition_for_picking_cancelation(
            self.location_id)
        quant = quant_obj.search(cond)
        quant.sudo().quantity = quant.quantity + self.qty_done

    def _quant_condition_for_picking_cancelation(self, location):
        cond = [('product_id', '=', self.product_id.id),
                ('location_id', '=', location.id)]
        if location.company_id:
            ('company_id', '=', location.company_id.id)
        if self.lot_id:
            cond.append(('lot_id', '=', self.lot_id.id))
        if self.package_id:
            cond.append(('package_id', '=', self.package_id.id))
        if self.owner_id:
            cond.append(('owner_id', '=', self.owner_id.id))
        return cond
