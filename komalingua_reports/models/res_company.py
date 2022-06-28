# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    custom_footer = fields.Boolean(
        string='Custom footer ', default=False)
    rml_footer = fields.Text(
        string='Report footer ')
