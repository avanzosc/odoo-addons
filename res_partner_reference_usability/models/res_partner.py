# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search_read(
            self, domain=None, fields=None, offset=0, limit=None, order=None):
        domain2 = False
        for d in domain:
            if d and d[0] == 'display_name':
                domain2 = [['ref', d[1], d[2]]]
        result = super(ResPartner, self).search_read(
            domain=domain, fields=fields, offset=offset, limit=limit,
            order=order)
        if domain2:
            result2 = super(ResPartner, self).search_read(
                domain=domain2, fields=fields, offset=offset, limit=limit,
                order=order)
            if result2:
                found = False
                for line in result2:
                    if line in result:
                        found = True
                if not found:
                    result += result2
        return result

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        result = super(ResPartner, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        if not name:
            return result
        my_name = '%{}%'.format(name)
        cond = [('ref', 'ilike', my_name)]
        partners = self.search(cond)
        for partner in partners:
            found = False
            for line in result:
                if line and line[0] == partner.id:
                    found = True
                    break
            if not found:
                result.append((partner.id, partner.name))
        return result
