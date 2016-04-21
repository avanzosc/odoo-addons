# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models, api


class WizPurchaseOrderSplit(models.TransientModel):
    _inherit = 'wiz.purchase.order.split'

    only_read = fields.Boolean(
        string='Only read', default=False)

    @api.model
    def default_get(self, fields):
        res = super(WizPurchaseOrderSplit, self).default_get(fields)
        pur_obj = self.env['purchase.order']
        proc_obj = self.env['procurement.order']
        for purchase in pur_obj.browse(self.env.context.get('active_ids')):
            for line in purchase.order_line:
                sproc = False
                cond = [('purchase_line_id', '=', line.id)]
                proc = proc_obj.search(cond, limit=1)
                if proc:
                    sproc = self._search_sale_procurement(proc, line)
                if sproc and sproc.sale_line_id.order_id.purchase_parts:
                    sale = sproc.sale_line_id.order_id
                    res.update({'parts': sale.purchase_parts,
                                'from_date': sale.purchase_from_date,
                                'each_month': sale.purchase_each_month,
                                'only_read': True})
                    break
            if res.get('from_date', False):
                break
        return res

    @api.multi
    def action_split_purchase_order(self):
        self.ensure_one()
        res = super(WizPurchaseOrderSplit, self).action_split_purchase_order()
        pur_obj = self.env['purchase.order']
        proc_obj = self.env['procurement.order']
        for purchase in pur_obj.browse(self.env.context.get('active_ids')):
            for line in purchase.order_line:
                sproc = False
                cond = [('purchase_line_id', '=', line.id)]
                proc = proc_obj.search(cond, limit=1)
                if proc:
                    sproc = self._search_sale_procurement(proc, line)
                if sproc and sproc.sale_line_id.order_id:
                    sale = sproc.sale_line_id.order_id
                    sale.write({'purchase_parts': self.parts,
                                'purchase_from_date': self.from_date,
                                'purchase_each_month': self.each_month})
                    cond = [('origin', '=', purchase.origin),
                            ('id', 'not in', sale.split_purchases.ids)]
                    purchases = pur_obj.search(cond)
                    for pur in purchases:
                        sale.split_purchases = [(4, pur.id)]
        return res

    def _search_sale_procurement(self, proc, line):
        proc_obj = self.env['procurement.order']
        sale_proc = self.env['procurement.order']
        cond = [('id', '<', proc.id),
                ('group_id', '=', proc.group_id.id),
                ('product_id', '=', proc.product_id.id),
                ('product_uos_qty', '=', proc.product_uos_qty),
                ('product_qty', '=', proc.product_qty),
                ('purchase_line_id', '=', False),
                ('sale_line_id', '!=', False)]
        sale_proc = proc_obj.search(cond, limit=1)
        return sale_proc
