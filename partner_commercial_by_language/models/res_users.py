# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResUsers(models.Model):
    _inherit = "res.users"

    commercial_lang_ids = fields.Many2many(
        comodel_name="res.lang",
        relation="user_comercial_lang_rel",
        column1="user_id",
        column2="lang_id",
        string="Languages",
        help="Link between users and comercial languages.",
    )

    def _get_crm_team(self):
        team_obj = self.env["crm.team"]
        self.ensure_one()
        return team_obj.search([("member_ids", "=", self.id)], limit=1)
