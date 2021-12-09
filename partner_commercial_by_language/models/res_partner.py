# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_default_commercial(self):
        """ Gives default commercial by language """
        lang_obj = self.env['res.lang']
        for partner in self:
            if partner.lang:
                lang = lang_obj.search([('code', '=', partner.lang)])
                return lang._get_commercial_from_team()

    user_id = fields.Many2one(default=_get_default_commercial)

    @api.onchange("lang")
    def onchange_lang(self):
        """This function returns value of commercial user based on partner language"""
        lang_obj = self.env['res.lang']
        if self.lang:
            lang = lang_obj.search([('code', '=', self.lang)])
            if lang.crm_team_id:
                self.user_id = lang._get_commercial_from_team()
                self.team_id = lang.crm_team_id
