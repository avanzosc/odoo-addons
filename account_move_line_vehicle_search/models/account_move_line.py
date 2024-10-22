from odoo import fields, models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    serial_number_id = fields.Many2one(
        "fleet.vehicle",
        "Serial Number",
        related="vehicle_id.serial_number_id",
        readonly=True,
    )
