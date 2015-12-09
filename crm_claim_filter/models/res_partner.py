# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if args is None:
            args = []
        partners = super(ResPartner, self).name_search(
            name, args=args, operator=operator, limit=limit)
        ids = [x[0] for x in partners]
        if name:
            ids2 = self.search(
                [('vat', operator, name)] + args, limit=limit).ids
            ids = list(set(ids + ids2))
        return self.browse(ids).name_get()
