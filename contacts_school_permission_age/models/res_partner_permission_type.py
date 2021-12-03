
from odoo import api, fields, models


class ResPartnerPermission(models.Model):
    _inherit = 'res.partner.permission.type'

    min_age = fields.Integer('Minimum signer age')
