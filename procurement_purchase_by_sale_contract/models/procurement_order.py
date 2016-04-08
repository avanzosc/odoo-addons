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
                if group == 'sale_contract':
                    proc._update_purchase_line_account_from_sale_account()
        return res

    @api.multi
    def make_po(self):
        res = {}
        for po in self:
            obj = po
            cond = [('id', '<', po.id),
                    ('product_uom', '=', po.product_uom.id),
                    ('product_uos_qty', '=', po.product_uos_qty),
                    ('product_qty', '=', po.product_qty),
                    ('product_uos', '=', po.product_uos.id),
                    ('state', '=', 'running'),
                    ('product_id', '=', po.product_id.id),
                    ('group_id', '=', po.group_id.id),
                    ('sale_line_id', '!=', False)]
            proc = self.search(cond, limit=1)
            if (proc.product_id.categ_id.procured_purchase_grouping ==
                    'sale_contract'):
                obj = po.with_context(
                    sale_contract=proc.sale_line_id.order_id.project_id)
            res = super(ProcurementOrder, obj).make_po()
        return res
