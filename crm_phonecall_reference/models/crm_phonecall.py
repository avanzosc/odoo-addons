# -*- coding: utf-8 -*-
# (c) 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api


class CrmPhonecall(models.Model):
    _inherit = 'crm.phonecall'

    @api.multi
    def _links_get(self):
        link_obj = self.env['res.request.link']
        return [(r.object, r.name) for r in link_obj.search([])]

    ref = fields.Reference(string='Reference', selection=_links_get)
    ref2 = fields.Reference(string='Reference 2', selection=_links_get)
    ref3 = fields.Reference(string='Reference 3', selection=_links_get)
