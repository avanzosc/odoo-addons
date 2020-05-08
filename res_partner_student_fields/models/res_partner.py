# Copyright (c) 2019 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    
    nickname = fields.Char(string='Nickname')
    priest = fields.Many2one(string='Priest', comodel_name='hr.employee')
    university = fields.Char(string='University')
    career = fields.Char(string='Career')
    
    
