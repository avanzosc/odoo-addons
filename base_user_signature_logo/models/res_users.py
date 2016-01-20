# coding: utf-8
from openerp import fields, models


class ResUsers(models.Model):
    _inherit = 'res.users'

    signature_logo = fields.Binary(string='Signature Logo')
