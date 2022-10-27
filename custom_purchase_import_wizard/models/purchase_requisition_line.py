# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    shipping_cost = fields.Float(
        string="Shipping Cost")
