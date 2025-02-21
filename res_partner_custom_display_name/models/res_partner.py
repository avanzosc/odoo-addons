from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    custom_display_name = fields.Char()

    @api.depends("custom_display_name", "name")
    def _compute_display_name(self):
        res = super()._compute_display_name()
        for partner in self:
            if partner.custom_display_name:
                partner.display_name = partner.custom_display_name
        return res
