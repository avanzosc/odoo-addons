
from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission.type'

    min_age = fields.Integer('Minimum signer age')

    def _compute_allowed_signer_ids(self):
        for record in self:
            permissions = self.env['res.partner.permission'].search([
                ('type_id', '=', record.id)
            ])
            permissions._compute_allowed_signer_ids()
