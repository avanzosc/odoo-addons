# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    portal_login_custom_text = fields.Html("Portal Login Custom Text")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    portal_login_custom_text = fields.Html(
        'Portal Login Custom Text',
        related='company_id.portal_login_custom_text', readonly=False)
