# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    @api.multi
    def button_create_plan(self):
        res = super(MrpProduction, self).button_create_plan()
        for production in self.filtered(lambda x: x.plan):
            production.plan._update_stock_information()
        return res
