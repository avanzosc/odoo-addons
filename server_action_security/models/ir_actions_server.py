# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class IrActionsServer(models.Model):
    _inherit = "ir.actions.server"

    groups_id = fields.Many2many(
        comodel_name="res.groups", relation="ir_actions_server_groups_rel",
        column1="action_id", column2="group_id", string="Groups")
