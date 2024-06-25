# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    analytic_line_ids = fields.One2many(
        string="Analytic Lines",
        comodel_name="account.analytic.line",
        inverse_name="account_move_id",
        copy=False,
    )

    def action_post(self):
        result = super().action_post()
        for line in self.invoice_line_ids:
            if line.account_id and line.account_id.analytic_template_ids:
                for template in line.account_id.analytic_template_ids:
                    analytic = self.env[("account.analytic.line")].create(
                        {
                            "name": line.account_id.name,
                            "account_id": template.account_analytic_id.id,
                            "move_id": line.id,
                            "date": line.move_id.date,
                        }
                    )
                    if template.percentage:
                        if line.credit:
                            analytic.amount = (template.percentage * line.credit) / 100
                        if line.debit:
                            analytic.amount = (
                                (-1) * template.percentage * line.debit
                            ) / 100
        return result

    def action_view_analytics(self):
        return {
            "name": _("Analytics"),
            "view_mode": "tree,form",
            "res_model": "account.analytic.line",
            "domain": [("id", "in", self.analytic_line_ids.ids)],
            "type": "ir.actions.act_window",
            "views": [
                [self.env.ref("analytic.view_account_analytic_line_tree").id, "tree"],
                [False, "form"],
            ],
            "context": self.env.context,
        }
