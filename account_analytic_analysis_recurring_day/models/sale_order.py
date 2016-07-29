# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        res = super(SaleOrder, self).action_button_confirm()
        for sale in self:
            if (sale.project_id and sale.project_id.recurring_invoices and
                    sale.project_id.recurring_rule_type == 'monthly'):
                if (not sale.project_id.recurring_first_day and not
                    sale.project_id.recurring_last_day and not
                        sale.project_id.recurring_the_day):
                    raise exceptions.Warning(
                        _('In the sale order %s, with contract: %s, you must'
                          ' indicate what day will generate the next invoice')
                        % (sale.name, sale.project_id.name))
        return res
