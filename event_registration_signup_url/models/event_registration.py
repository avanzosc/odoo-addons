# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    user_id = fields.Many2one(
        string='User', comodel_name='res.users', related='student_id.user_id',
        store=True)
    signup_url = fields.Char(
        string='Sign Up URL', related='user_id.signup_url', store=True)
