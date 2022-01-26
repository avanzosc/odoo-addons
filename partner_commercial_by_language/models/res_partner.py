# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    def _get_default_commercial(self):
        """ Gives default commercial by language """
        lang_obj = self.env["res.lang"]
        for partner in self:
            if partner.lang and not partner.parent_id:
                lang = lang_obj.search([("code", "=", partner.lang)])
                return lang._get_commercial_from_team()

    user_id = fields.Many2one(default=_get_default_commercial)

    @api.onchange("lang")
    def onchange_lang(self):
        """This function returns value of commercial user based on partner language"""
        lang_obj = self.env["res.lang"]
        if self.lang and not self.parent_id:
            lang = lang_obj.search([("code", "=", self.lang)])
            user = lang._get_commercial_from_team()
            if user:
                self.user_id = user
                self.team_id = user._get_crm_team()

    # Inherited to reply on connector process
    def create(self, vals_list):
        res = super(ResPartner, self).create(vals_list)
        if res and not res.user_id and not res.parent_id:
            res.onchange_lang()
        elif res and not res.user_id and res.parent_id and res.parent_id.user_id:
            res.user_id = res.parent_id.user_id
        return res
