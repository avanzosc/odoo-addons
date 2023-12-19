# Copyright 2021 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    def action_discontinue(self, date=False):
        self.ensure_one()
        if not date:
            date = fields.Date.context_today(self)
        student_contracts = self.env["contract.contract"].sudo().search([
            ("child_id", "=", self.id)])
        reason = self.env.ref(
            "contract_sale_school.contract_terminate_reason_discontinued")
        for contract in student_contracts:
            contract.sudo()._terminate_contract(
                reason, _("{} by {}".format(reason.name,
                                            self.env.user.display_name)),
                date)
        super().action_discontinue(date=date)
