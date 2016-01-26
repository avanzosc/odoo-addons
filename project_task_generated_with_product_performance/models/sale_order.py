# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        project_obj = self.env['project.project']
        if not self.project_id:
            raise exceptions.Warning(_('You must enter the project/contract'))
        if not self.project_id.date_start:
            raise exceptions.Warning(_('You must enter the start date of the'
                                       ' project/contract'))
        if not self.project_id.date:
            raise exceptions.Warning(_('You must enter the end date of the'
                                       ' project/contract'))
        cond = [('analytic_account_id', '=', self.project_id.id)]
        project = project_obj.search(cond, limit=1)
        if not project:
            raise exceptions.Warning(_('Project/contract without project'))
        res = super(SaleOrder, self).action_button_confirm()
        return res
