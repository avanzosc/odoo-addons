# Copyright 2026 Ane Gurruchaga - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

class ResCompany(models.Model):
    _inherit = "res.company"
    
    fsc_certificate_image = fields.Binary(string="FSC Certificate Logo")
    fsc_certificate_number = fields.Char(string="FSC Certificate Number")
