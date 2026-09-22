# Copyright 2019 Alejandro Nieto - Okatent
# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class purchase_order_note(models.Model):
    _inherit = "purchase.order"

    purchase_order_note = fields.Char(string="Notes")
