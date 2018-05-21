# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_group = fields.Many2one(
        comodel_name='res.partner', string='Partner Group')
    is_group = fields.Boolean(
        string='Is a Group', help="Check if the partner is a group")
