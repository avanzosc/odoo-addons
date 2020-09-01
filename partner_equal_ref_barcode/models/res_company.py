# Copyright (c) 2020 Adrian Revilla <adrianrevilla@avanzosc.es> - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    partner_barcode_unique = fields.Selection(
        selection=[
            ('none', 'None'),
            ('companies', 'Only companies'),
            ('all', 'All partners'),
        ], string="Unique partner barcode for", default="none")
