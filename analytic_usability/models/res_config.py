# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_show_invoice_data = fields.Boolean(
        string="Show Invoice Data in Analytic Entries",
        implied_group="analytic_usability.group_show_invoice_data")
