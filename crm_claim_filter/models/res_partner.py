# -*- coding: utf-8 -*-
# (c) 2015 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    def name_search(self, cr, uid, name, args=None, operator='ilike',
                    context=None, limit=100):
        if args is None:
            args = []
        partners = super(ResPartner, self).name_search(
            cr, uid, name, args=args, operator=operator, context=context,
            limit=limit)
        ids = [x[0] for x in partners]
        if name:
            ids = self.search(cr, uid,
                              ['|', ('id', 'in', ids),
                               ('vat', operator, name)],
                              limit=limit, context=context)
        return self.name_get(cr, uid, ids, context=context)
