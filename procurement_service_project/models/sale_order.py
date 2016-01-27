# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        procurement_obj = self.env['procurement.order']
        procurement_group_obj = self.env['procurement.group']
        res = super(SaleOrder, self).action_button_confirm()
        for line in self.order_line:
            valid = self._validate_service_project_for_procurement(
                line.product_id)
            if valid:
                if not self.procurement_group_id:
                    vals = self._prepare_procurement_group(self)
                    group = procurement_group_obj.create(vals)
                    self.write({'procurement_group_id': group.id})
                vals = self._prepare_order_line_procurement(
                    self, line, group_id=self.procurement_group_id.id)
                vals['name'] = self.name + ' - ' + line.product_id.name
                procurement = procurement_obj.create(vals)
                procurement.run()
        return res

    def _validate_service_project_for_procurement(self, product):
        routes = product.route_ids.filtered(lambda r: r.id in [
            self.env.ref('procurement_service_project.route_serv_project').id])
        return product.type == 'service' and routes


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    service_project_task = fields.Many2one(
        'project.task', string='Generated task from procurement')
