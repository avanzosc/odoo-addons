# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    odoo_category = fields.Many2one(
        comodel_name='odoo.partner.category')
    odoo_logo_report = fields.Boolean(
        string='Odoo partner logo on report', default=False,
        help='If checked the corresponding logo will be shown right side of '
        'header')
    odoo_partner_logo = fields.Binary(related='odoo_category.logo')
