# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    import_unpaid_invoices = fields.Monetary(
        string="Invoices unpaid amount",
        related="partner_id.import_unpaid_invoices",
        groups="account.group_account_invoice,account.group_account_readonly",
    )
