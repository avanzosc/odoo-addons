from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    barcode_format_ids = fields.Many2many(
        "barcode.format",
        string="Barcode Formats",
        relation="barcode_format_partner_rel",
        column1="partner_id",
        column2="format_id",
    )

    @api.depends("barcode_format_ids.partner_ids")
    def _compute_barcode_format_ids(self):
        for partner in self:
            partner.barcode_format_ids = self.env["barcode.format"].search(
                [("partner_ids", "in", partner.id)]
            )
