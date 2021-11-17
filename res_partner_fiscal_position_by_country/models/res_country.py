# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    default_incoterm_id = fields.Many2one(
        "account.incoterms", "Default Incoterm")
