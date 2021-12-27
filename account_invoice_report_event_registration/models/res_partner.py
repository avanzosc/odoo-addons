# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    invoice_report_print_students = fields.Boolean(
        string='Print students in invoice report', default=False)
