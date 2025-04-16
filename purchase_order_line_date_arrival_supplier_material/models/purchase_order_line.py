# Copyright 2025 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseorderLine(models.Model):
    _inherit = "purchase.order.line"

    date_arrival_supplier_material = fields.Date(copy=False)
