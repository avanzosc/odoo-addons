# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ProductCategory(models.Model):
    _inherit = "product.category"

    not_show_in_inventory_reports = fields.Boolean(
        string="NOT show in inventory reports", default=False, copy=False)
