# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        event_obj = self.env['event.event']
        project_obj = self.env['project.project']
        res = super(SaleOrder, self).action_button_confirm()
        for sale in self:
            if sale.project_id.festive_calendars:
                cond = [('analytic_account_id', '=', sale.project_id.id)]
                project = project_obj.search(cond, limit=1)
                cond = [('project_id', '=', project.id)]
                events = event_obj.search(cond)
                for event in events:
                    event._put_festives_in_sesions_from_sale_contract(
                        sale.project_id.festive_calendars)
        return res
