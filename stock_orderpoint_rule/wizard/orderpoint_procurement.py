# -*- coding: utf-8 -*-
# © 2016 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, api


class ProcurementCompute(models.TransientModel):

    _inherit = 'procurement.orderpoint.compute'

    @api.multi
    def selected_procure_calculation(self):
        self.with_context(
            {'orderpoints_ids': self._context.get(
                'active_ids')}).procure_calculation()
