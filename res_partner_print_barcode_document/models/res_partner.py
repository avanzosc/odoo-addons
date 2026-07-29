from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    print_barcode = fields.Boolean(string="Print Barcodes In Reports", default=True)
