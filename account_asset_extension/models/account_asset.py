# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class AccountAssetAsset(models.Model):
    _inherit = 'account.asset.asset'

    real_purchase_date = fields.Date(String='Real purchase date')
    real_purchase_amount = fields.Float(String='Real purchase amount')
