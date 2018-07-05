# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResPartnerArea(models.Model):
    _name = 'res.partner.area'
    _description = 'Partner Areas'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
