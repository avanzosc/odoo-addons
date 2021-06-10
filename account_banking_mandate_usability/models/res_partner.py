# Copyright 2021 Daniel Campos - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    bank_acc_count = fields.Integer(
        compute="_compute_bank_acc_count", string="Number of Bank accounts",
        readonly=True)

    def _compute_bank_acc_count(self):
        bank_acc_data = self.env["res.partner.bank"].read_group(
            [("partner_id", "in", self.ids)], ["partner_id"], ["partner_id"]
        )
        mapped_data = {
            bank_acc["partner_id"][0]: bank_acc["partner_id_count"]
            for bank_acc in bank_acc_data
        }
        for partner in self:
            partner.bank_acc_count = mapped_data.get(partner.id, 0)
