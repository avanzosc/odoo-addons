# -*- coding: utf-8 -*-
# Copyright 2020 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, models, fields, api


class ResPartnerCnae(models.Model):
    _name = "res.partner.cnae"
    _description = "CNAE codes"

    code = fields.Char(
        string="Code", required=True
    )
    name = fields.Char(
        string="Description", required=True
    )

    def name_get(self):
        new_res = []
        for line in self:
            name = u"[{}] {}".format(line.code, line.name)
            new_res.append((line.id, name))
        return new_res

    @api.model
    def name_search(self, name, args=None, operator="ilike", limit=100):
        args = args or []
        recs = self.browse()
        if name:
            recs = self.search([("code", "=", name)] + args, limit=limit)
        if not recs:
            recs = self.search([("name", operator, name)] + args, limit=limit)
        return recs.name_get()
