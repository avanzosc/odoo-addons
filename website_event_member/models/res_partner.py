
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_member = fields.Boolean(string='Is member?', default=False)

    def action_make_members(self):
        for rec in self:
            rec.is_member = True
