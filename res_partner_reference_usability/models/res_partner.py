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
