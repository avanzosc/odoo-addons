# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    school_ids = fields.Many2many(
        comodel_name='res.partner', name='Schools',
        domain=[('educational_category', '=', 'school')])
