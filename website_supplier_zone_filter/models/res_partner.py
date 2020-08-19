# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    sends_to = fields.Selection(
        selection=[('city', 'City'),
                   ('zone', 'Zone'),
                   ('state', 'State'),
                   ('all', 'All')], string='Sends to')
