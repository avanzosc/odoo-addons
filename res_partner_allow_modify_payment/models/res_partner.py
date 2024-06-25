# Copyright 2023 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    allow_modify_payment = fields.Boolean(
        string="Allow modify payment", compute="_compute_allow_modify_payment"
    )

    def _compute_allow_modify_payment(self):
        group = self.env.ref(
            "res_partner_allow_modify_payment.group_allow_mod_partner_payment"
        )
        allow_modify_payment = True if self.env.user in group.users else False
        for partner in self:
            partner.allow_modify_payment = allow_modify_payment
