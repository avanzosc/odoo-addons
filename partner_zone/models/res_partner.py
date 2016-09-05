# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields, models


class ResPartnerZone(models.Model):
    _name = 'res.partner.zone'

    name = fields.Char(string='Name')


class ResPartner(models.Model):
    _inherit = 'res.partner'

    zone_ids = fields.Many2many(
        comodel_name='res.partner.zone', relation='rel_partner_zone',
        column1='zone_id', column2='partner_id', string='Zones')
