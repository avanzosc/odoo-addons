# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'

    @api.multi
    def write(self, values):
        res = super(ProcurementOrder, self).write(values)
        if 'purchase_line_id' in values:
            for proc in self:
                if (proc.sale_line_id and
                    proc.sale_line_id.delivery_standard_price and
                    proc.purchase_line_id and
                        self._is_procurement_service(proc)):
                    name = proc.purchase_line_id.name
                    name += ', ' + proc.origin + ', ' + str(proc.date_planned)
                    proc.purchase_line_id.write({
                        'name': name,
                        'price_unit':
                        proc.sale_line_id.delivery_standard_price})
        return res
