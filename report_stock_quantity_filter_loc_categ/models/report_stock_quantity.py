# Copyright 2022 AlfredodelaFuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ReportStockQuantity(models.Model):
    _inherit = "report.stock.quantity"

    not_show_category_in_inventory_reports = fields.Boolean(
        string="NOT show category in inventory reports", readonly=True)
    not_show_location_in_inventory_reports = fields.Boolean(
        string="NOT show location in inventory reports", readonly=True)
