# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, _


class WizCreateProcurementStockInfo(models.TransientModel):
    _name = 'wiz.create.procurement.stock.info'
    _description = 'Wizard for create procurements from stock info'

    @api.multi
    def create_procurement_orders(self):
        self.ensure_one()
        info_obj = self.env['stock.information']
        proc_obj = self.env['procurement.order']
        all_informations = info_obj.browse(self.env.context.get('active_ids'))
        informations = all_informations.filtered(lambda x: x.virtual_stock > 0)
        for stock_info in informations:
            stock_vals = self._prepare_procurement_vals(stock_info)
            proc = proc_obj.create(stock_vals)
            rule_id = proc_obj._find_suitable_rule(proc)
            if rule_id:
                proc.write({'rule_id': rule_id})

    @api.multi
    def _prepare_procurement_vals(self, stock_info):
        date_planned = stock_info.first_day_week + ' 00:00:01'
        vals = {'company_id': stock_info.company.id,
                'product_id': stock_info.product.id,
                'product_uom': stock_info.product.uom_id.id,
                'product_qty': stock_info.virtual_stock,
                'location_id': stock_info.location.id,
                'origin': _('From stock information'),
                'name': _('Created from stock information'),
                'date_planned': date_planned,
                'priority': '1',
                'state': 'confirmed'}
        return vals
