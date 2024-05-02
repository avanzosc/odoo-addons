# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class AccountInvoiceLine(models.Model):
    _inherit = "account.move.line"

    lot_ids = fields.Many2many(
        comodel_name="stock.production.lot",
        string="lots",
        relation="rel_invoice_line_lot",
        column1="invoice_line_id",
        column2="lot_id",
    )
