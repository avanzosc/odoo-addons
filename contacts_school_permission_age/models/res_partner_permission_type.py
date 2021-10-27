
from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission.type'

    min_age = fields.Integer('Minimum signer age')

    @api.onchange('min_age')
    def _onchange_min_age(self):
        permissions = self.env['res.partner.permission'].search([
            ('type_id', '=', self._origin.id)
        ])
        permissions._compute_allowed_signer_ids()
