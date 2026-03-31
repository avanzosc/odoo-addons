# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    penalty_warning_id = fields.Many2one(
        string="Penalty warning", comodel_name="penalty.warning", copy=False
    )
    penalty_warning_description = fields.Char(
        string="Penalty warning description", related="penalty_warning_id.description"
    )
