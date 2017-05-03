# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class ProcurementCompute(models.TransientModel):

    _inherit = 'procurement.orderpoint.compute'

    @api.multi
    def selected_procure_calculation(self):
        if (self.env.context.get('active_model', False) ==
                'stock.warehouse.orderpoint'):
            self.with_context(
                {'orderpoints_ids': self._context.get(
                    'active_ids')}).procure_calculation()
        elif (self.env.context.get('active_model', False) ==
                'procurement.order'):
            products = self.env['procurement.order'].browse(
                self.env.context.get('active_ids')).mapped('product_id')
            cond = [('product_id', 'in', products.ids)]
            orderpoints = self.env['stock.warehouse.orderpoint'].search(cond)
            self.with_context(
                {'orderpoints_ids': orderpoints.ids}).procure_calculation()
        else:
            self.procure_calculation()
