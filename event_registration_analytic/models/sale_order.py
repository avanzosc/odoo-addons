# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, fields


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_by_task = fields.Selection(
        [('yes', 'Yes'),
         ('no', 'No')], string='Create project by task')

    @api.multi
    def action_button_confirm(self):
        project_obj = self.env['project.project']
        event_obj = self.env['event.event']
        res = super(SaleOrder, self).action_button_confirm()
        cond = [('analytic_account_id', '=', self.project_id.id)]
        project = project_obj.search(cond, limit=1)
        cond = [('project_id', '=', project.id)]
        events = event_obj.search(cond)
        for event in events:
            tickets = event.event_ticket_ids.filtered(
                lambda x: x.product_id.id ==
                self.env.ref('event_sale.product_product_event').id)
            tickets.unlink()
        return res
