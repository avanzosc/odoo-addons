# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    check_lot_is_under_warranty = fields.Boolean(
        string="Check Repair Lot Is Under Warranty", default=True
    )
