# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _renovate_sale_and_contract_from_wizard(self):
        for sale in self:
            sale.project_id._renovate_contract_from_wizard(0, sale)
