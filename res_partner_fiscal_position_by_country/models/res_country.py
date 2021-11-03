
from odoo import api, fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    default_incoterm_id = fields.Many2one(
        "account.incoterms", "Default Incoterm")
