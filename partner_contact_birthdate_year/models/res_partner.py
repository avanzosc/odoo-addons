# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def _compute_partner_years(self):
        for partner in self:
            if partner.birthdate_date:
                today = fields.Date.context_today(self)
                difference = (fields.Date.from_string(today) -
                              fields.Date.from_string(partner.birthdate_date))
                partner.years = difference.days / 365

    age = fields.Integer(compute='_compute_partner_years')
