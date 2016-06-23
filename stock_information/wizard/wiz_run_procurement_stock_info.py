# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class WizRunProcurementStockInfo(models.TransientModel):
    _name = 'wiz.run.procurement.stock.info'
    _description = 'Wizard for run procurements from stock info'

    @api.multi
    def run_procurement_orders(self):
        self.ensure_one()
        info_obj = self.env['stock.information']
        for information in info_obj.browse(self.env.context.get('active_ids')):
            for procurement in information.demand_procurements:
                procurement.run()
