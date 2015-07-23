# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class OdooPartnerCategory(models.Model):
    _name = 'odoo.partner.category'

    name = fields.Char()
    logo = fields.Binary(string='Odoo Partner Logo')
