# Copyright 2026 Aner Arregi - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "agreement"

    agreement_penalty_ids = fields.One2many(
        comodel_name="agreement.penalty.type",
        inverse_name="agreement_id",
        string="Penalty Types",
    )
