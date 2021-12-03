
from odoo import api, fields, models


class ResPartnerPermissionType(models.Model):
    _inherit = 'res.partner.permission.type'

    min_age = fields.Integer('Minimum signer age')
