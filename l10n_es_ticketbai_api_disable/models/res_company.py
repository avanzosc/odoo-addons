from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    tbai_enabled = fields.Boolean(default=False)

    @api.model
    def create(self, vals):
        vals["tbai_enabled"] = False
        return super().create(vals)

    def write(self, vals):
        if "tbai_enabled" in vals:
            vals["tbai_enabled"] = False
        return super().write(vals)

    @api.model
    def _set_tbai_enabled_false(self):
        companies = self.search([("tbai_enabled", "!=", False)])
        companies.write({"tbai_enabled": False})
