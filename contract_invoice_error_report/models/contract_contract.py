# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ContractContract(models.Model):
    _inherit = "contract.contract"

    with_invoice_generation_error = fields.Boolean(
        string="With invoice generation error", default=False, copy=False
    )
    invoice_generation_error = fields.Char(
        string="Invoice generation error", copy=False
    )
