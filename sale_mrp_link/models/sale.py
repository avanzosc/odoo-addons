# -*- coding: utf-8 -*-
# © 2015 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    mrp_production_id = fields.One2many(
        comodel_name='mrp.production', string='Mrp Production',
        inverse_name='sale_line')

    @api.multi
    def need_procurement(self):
        for line in self:
            if line.mrp_production_id:
                return False
            else:
                return super(SaleOrderLine, self).need_procurement()


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        lines = self.order_line.filtered(
            lambda x: x.mrp_production_id is not False)
        for line in lines:
            for mrp in line.mrp_production_id:
                mrp.write(
                    {'show': True,
                     'sale_order': self.id,
                     'partner': self.partner_id.id})
        return res
