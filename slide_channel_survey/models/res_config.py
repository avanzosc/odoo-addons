from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    certification_header_image = fields.Binary("Certifications Header Image")


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    certification_header_image = fields.Binary(
        "Certifications Header Image",
        related="company_id.certification_header_image",
        readonly=False,
    )
