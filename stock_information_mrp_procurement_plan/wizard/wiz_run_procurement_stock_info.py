# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizRunProcurementStockInfo(models.TransientModel):
    _inherit = 'wiz.run.procurement.stock.info'

    @api.multi
    def run_procurement_orders(self):
        self.ensure_one()
        super(WizRunProcurementStockInfo, self).run_procurement_orders()
        info_obj = self.env['stock.information']
        for information in info_obj.browse(self.env.context.get('active_ids')):
            for procurement in information.incoming_pending_procurements_plan:
                procurement.run()
            procs = information.incoming_pending_procurements_plan_reservation
            for procurement in procs:
                procurement.run()
