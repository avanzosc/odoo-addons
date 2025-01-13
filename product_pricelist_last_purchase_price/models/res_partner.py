# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    not_update_price_from_order = fields.Boolean(
        string="Not Update Price From Order", default=False
    )
    not_update_price_from_invoice = fields.Boolean(
        string="Not Update Price From Invoice", default=False
    )
