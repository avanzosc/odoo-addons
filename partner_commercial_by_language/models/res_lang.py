# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResLang(models.Model):
    _inherit = "res.lang"

    crm_team_id = fields.Many2one(string='CRM Team', comodel_name='crm.team')

    def _get_commercial_from_team(self):
        if self.crm_team_id and self.crm_team_id.member_ids:
            new_commercial = False
            for member in self.crm_team_id.member_ids.sorted(key=lambda r: r.name):
                if not self.crm_team_id.last_comercial_id or \
                        self.crm_team_id.last_comercial_id.name < member.name:
                    new_commercial = member
                    break
            if not new_commercial:
                new_commercial = self.crm_team_id.member_ids.sorted(
                    key=lambda r: r.name)[0]
            self.crm_team_id.last_comercial_id = new_commercial
            return new_commercial
