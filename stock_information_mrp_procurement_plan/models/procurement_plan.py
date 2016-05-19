# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api, _


class ProcurementPlan(models.Model):
    _inherit = 'procurement.plan'

    @api.multi
    def button_recalculate_stock_info(self):
        wiz_obj = self.env['wiz.stock.information']
        info_obj = self.env['stock.information']
        products = self.env['product.product']
        max_fec = False
        cond = []
        informations = info_obj.search(cond)
        if informations:
            max_stock_info = max(informations, key=lambda x: x.last_day_week)
            if max_stock_info:
                max_fec = max_stock_info.last_day_week
        for plan in self:
            if plan.procurement_ids:
                products |= plan.procurement_ids.mapped('product_id')
                max_proc = max(
                    plan.procurement_ids, key=lambda x: x.date_planned)
                if max_proc:
                    if not max_fec or max_proc.date_planned > max_fec:
                        max_fec = max_proc.date_planned
        wiz_vals = {'company': self.env.user.company_id.id,
                    'to_date': max_fec}
        wiz = wiz_obj.create(wiz_vals)
        cond = [('company', '=', self.env.user.company_id.id),
                ('product', 'in', products.ids)]
        informations = info_obj.search(cond)
        informations.unlink()
        to_date = info_obj._calculate_last_day_week(
            fields.Datetime.from_string(wiz.to_date).date())
        product_datas = wiz._cath_moves_and_procurements(to_date, products.ids)
        info_obj._generate_stock_information(wiz, product_datas)
        return {'name': _('Stock information'),
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree',
                'res_model': 'stock.information',
                'domain': [('product', 'in', products.ids)]}
