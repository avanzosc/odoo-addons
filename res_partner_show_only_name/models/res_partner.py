# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    @api.multi
    def name_get(self):
        return models.Model.name_get(self)

    @api.model
    def name_search(self, name, args=None, operator='ilike', context=None,
                    limit=100):
        return models.Model.name_search(
            self, name=name, args=args, operator=operator, limit=limit)
