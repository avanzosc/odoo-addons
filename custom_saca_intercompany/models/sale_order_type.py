# © 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See https://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class SaleOrderType(models.Model):
    _inherit = "sale.order.type"

    license_plate = fields.Char(string="License Plate")
