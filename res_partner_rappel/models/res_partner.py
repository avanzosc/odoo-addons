# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    partner_rappel_ids = fields.One2many(
        string="Partner Rappel",
        comodel_name="res.partner.rappel",
        inverse_name="partner_id",
    )

    def action_view_rappel(self):
        return {
            "name": _("Rappels"),
            "view_mode": "tree",
            "res_model": "account.move.line",
            "domain": [
                ("partner_rappel_id", "!=", False),
                ("partner_id", "=", self.id),
            ],
            "type": "ir.actions.act_window",
            "views": [[self.env.ref("res_partner_rappel.rappel_view_tree").id, "tree"]],
            "context": self.env.context,
        }
