# Copyright 2021 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Company(models.Model):
    _inherit = 'res.company'

    portal_user_default_domain = fields.Char("Portal User Default Domain")


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    portal_user_default_domain = fields.Char(
        'Portal User Default Domain',
        related='company_id.portal_user_default_domain', readonly=False)
