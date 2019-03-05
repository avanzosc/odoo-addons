# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    po_double_validation_amount2 = fields.Monetary(
        related='company_id.po_double_validation_amount2',
        string="Secondary Minimum Amount",
        currency_field='company_currency_id')
