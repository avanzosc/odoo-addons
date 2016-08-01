# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class Website(models.Model):
    _inherit = 'website'

    google_remarketing_code = fields.Char(string='Google Remarketing Code')
