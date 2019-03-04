# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    group_show_accounting_date = fields.Boolean(
        string="Show Accounting Date in Vendor Bills",
        implied_group="account_utilities.group_show_accounting_date")
    group_show_account_invoice_line_menu = fields.Boolean(
        string="Show Menu To Account Invoice Lines",
        implied_group="account_utilities.group_show_account_invoice_line_menu")
