# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def write(self, vals):
        res = super(ProcurementOrder, self).write(vals)
        if 'purchase_line_id' in vals:
            for proc in self:
                group = proc.product_id.categ_id.procured_purchase_grouping
                if group == 'line':
                    proc._update_purchase_line_account_from_sale_account()
        return res

    def _update_purchase_line_account_from_sale_account(self):
        cond = [('id', '<', self.id),
                ('product_uom', '=', self.product_uom.id),
                ('product_uos_qty', '=', self.product_uos_qty),
                ('product_qty', '=', self.product_qty),
                ('product_uos', '=', self.product_uos.id),
                ('state', '=', 'running'),
                ('product_id', '=', self.product_id.id),
                ('group_id', '=', self.group_id.id),
                ('sale_line_id', '!=', False)]
        proc = self.search(cond, limit=1)
        if proc.sale_line_id.order_id.project_id:
            self.purchase_line_id.account_analytic_id = (
                proc.sale_line_id.order_id.project_id.id)
