# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, api, exceptions, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_button_confirm(self):
        if not self.project_id:
            raise exceptions.Warning(_('You must enter the project/contract'))
        return super(SaleOrder, self).action_button_confirm()
