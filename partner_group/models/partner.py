# -*- coding: utf-8 -*-
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_group = fields.Many2one('res.partner', 'Partner Group')
    is_group = fields.Boolean('Is a Group',
                              help="Check if the partner is a group")
