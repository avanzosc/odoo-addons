# -*- coding: utf-8 -*-
from odoo import models, fields

class ResCompany(models.Model):
    _inherit = "res.company"

    html_info = fields.Text(
        string="Additional HTML Info",
        help="Additional information in HTML format to be displayed on the contact page.",
    )
