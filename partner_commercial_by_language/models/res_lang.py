# Copyright (c) 2021 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResLang(models.Model):
    _inherit = "res.lang"

    commercial_user_id = fields.Many2one(string='Commercial', comodel_name='res.users')
