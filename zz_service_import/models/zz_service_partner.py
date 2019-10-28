# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class zzServicePartner(models.Model):
    _inherit = 'res.partner'
    shelf_number = fields.Integer(string='Numero de balda')
    p = fields.Integer(string='P')
    c = fields.Integer(string='C')
    n = fields.Integer(string='N')
    b = fields.Integer(string='B')
    a = fields.Integer(string='A')
    quantity = fields.Float(string='Importe')