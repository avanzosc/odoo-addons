from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = "res.partner"

    barcode_format_ids = fields.One2many(
        comodel_name="barcode.format",
        compute="_compute_barcode_format_ids",
        string="Formatos de código de barras",
        readonly=True
    )

    @api.depends('barcode_format_ids.partner_ids')
    def _compute_barcode_format_ids(self):
        for partner in self:
            partner.barcode_format_ids = self.env['barcode.format'].search([
                ('partner_ids', 'in', partner.id)
            ])
