from odoo import api, models


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def fields_get(self, *args, **kwargs):
        # switch to superuser to get access to virtual fields
        return super(ResUsers, self.sudo()).fields_get(*args, **kwargs)
