# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    po_double_validation_amount2 = fields.Monetary(
        string='Secondary Double validation amount', default=10000,
        help="Minimum amount for which a double validation is required")
