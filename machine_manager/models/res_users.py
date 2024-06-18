# Copyright 2015 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    machine_ids = fields.Many2many(
        string="Machines",
        comodel_name="machine",
        relation="machine_user_rel",
        column1="user_id",
        column2="machine_id",
    )
