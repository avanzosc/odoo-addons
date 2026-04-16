# Copyright 2026 Lucía Echeverría - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Agreement(models.Model):
    _inherit = "account.penalty"

    agreement_id = fields.Many2one(
        comodel_name="agreement",
        string="Agreement",
    )

    affected_subscription = fields.Integer(string="Affected Subs.")
