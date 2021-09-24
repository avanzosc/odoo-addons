# Copyright 2021 Berezi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    user_id = fields.Many2one(string='User', comodel_name='res.users')
