# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    requisition_origin = fields.Char(
        string="Requisition Origin", related="requisition_id.origin", store=True
    )
