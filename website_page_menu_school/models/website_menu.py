# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    school_id = fields.Many2one(
        string='School', comodel_name='res.partner',
        domain=[('educational_category', '=', 'school')])
