# Copyright 2019 Alejandro Nieto - Okatent
# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class Picking(models.Model):
    _inherit = "stock.picking"

    account_analytic_purchase_order = fields.Many2one(
        related="purchase_id.analytic_account_id",
        string="Project",
        store=True,
        readonly=True,
    )
