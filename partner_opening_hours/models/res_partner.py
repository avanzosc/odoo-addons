# Copyright 2018 Eider Oyarbide - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.htmljoze

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    opening_hours_id = fields.Many2one(
        comodel_name='resource.calendar',
        string='Opening hours')
