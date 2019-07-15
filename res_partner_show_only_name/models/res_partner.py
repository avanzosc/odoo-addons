# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    @api.multi
    def name_get(self):
        res = []
        for record in self:
            name_list = super(ResPartner, record).name_get()
            for name in name_list:
                if record.parent_id and not record.is_company:
                    name2replace = u"{}, {}".format(
                        record.parent_name, record.name)
                    name = list(name)
                    name[1] = name[1].replace(name2replace, record.name)
                    name = tuple(name)
                res.append(name)
        return res

    @api.model
    def name_search(self, name, args=None, operator='ilike', context=None,
                    limit=100):
        return models.Model.name_search(
            self, name=name, args=args, operator=operator, limit=limit)
