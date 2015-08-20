# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def write(self, values):
        res = super(ProcurementOrder, self).write(values)
        if 'purchase_line_id' in values:
            for proc in self:
                routes = proc.product_id.route_ids.filtered(
                    lambda r: r.name in ('Make To Order', 'Buy'))
                if (proc.sale_line_id and
                    proc.sale_line_id.delivery_standard_price and
                    proc.purchase_line_id and proc.product_id.type == 'service'
                        and len(routes) == 2):
                    name = proc.purchase_line_id.name
                    name += ', ' + proc.origin + ', ' + str(proc.date_planned)
                    proc.purchase_line_id.write(
                        {'name': name,
                         'price_unit':
                         proc.sale_line_id.delivery_standard_price})
        return res
