# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResLang(models.Model):
    _inherit = "res.lang"

    last_comercial_id = fields.Many2one(
        string="Last Commercial", comodel_name="res.users"
    )

    def _get_commercial_from_team(self):
        users_obj = self.env["res.users"]
        users_dict = {}
        for user in users_obj.search([]):
            if self.id in user.commercial_lang_ids.ids:
                team_id = user._get_crm_team()
                if team_id:
                    users_dict.update(
                        {user.id: {"user_name": user.name, "user_team": team_id}}
                    )
        new_commercial = False
        if users_dict:
            for user_data in users_dict.items():
                if (
                    not self.last_comercial_id
                    or self.last_comercial_id.name < user_data[1]["user_name"]
                ):
                    new_commercial = users_obj.browse(user_data[0])
                    break
            if not new_commercial:
                sorted_dict = sorted(
                    users_dict.items(), key=lambda item: item[1]["user_name"]
                )
                new_commercial = users_obj.browse(sorted_dict[0][0])
            self.last_comercial_id = new_commercial
        return new_commercial
