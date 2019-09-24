# -*- encoding: utf-8 -*-
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        results = super(ResPartner, self).name_search(name, args,
                                                      operator, limit)
        results += self.search(
            [('vat', operator, name)] + args, limit=limit).name_get()
        return results

    @api.multi
    def name_get(self):
        results = []
        for partner in self:
            result = super(ResPartner, partner).name_get()
            for partner_id, name in result:
                if partner.vat:
                    name = u'[{}] {}'.format(partner.vat, name)
                results.append(tuple([partner_id, name]))
        return results
