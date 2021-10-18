
from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission.type'

    min_age = fields.Integer('Minimum signer age')

    @api.onchange('min_age')
    def _apply_age_filter_signers(self):
        for record in self:
            permissions = self.env['res.partner.permission'].search([
                ('type_id', '=', record.id)
            ])
            permissions._compute_allowed_student_ids()
