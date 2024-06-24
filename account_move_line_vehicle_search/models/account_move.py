from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    vehicle_id = fields.Many2one(
        "fleet.vehicle",
        string="Vehicle",
        related="line_ids.vehicle_id",
        readonly=True,
    )

    serial_number_id = fields.Many2one(
        "fleet.vehicle",
        string="Serial Number",
        related="line_ids.serial_number_id",
        readonly=True,
    )
