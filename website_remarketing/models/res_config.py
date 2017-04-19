# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models


class WebsiteConfigSettings(models.Model):
    _inherit = 'website.config.settings'

    google_remarketing_code = fields.Char(
        related='website_id.google_remarketing_code',
        string='Google Remarketing Code')
