# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = 'res.users'

    headquarter_ids = fields.Many2many(
        string='Headquarters', comodel_name='res.partner',
        relation='rel_user_headquarter', column1='user_id',
        column2='headquarter_id',
        domain="[('headquarter','=', True)]")
