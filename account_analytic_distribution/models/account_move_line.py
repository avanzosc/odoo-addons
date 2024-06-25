# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_reference = fields.Char(
        string="Paymente Reference", related="move_id.payment_reference"
    )
    distribution_done = fields.Boolean(
        string="Distribution Done", compute="_compute_distribution_done", store=True
    )
    account_name = fields.Char(
        string="Account Name", related="account_id.name", store=True
    )

    @api.depends(
        "credit",
        "debit",
        "analytic_line_ids",
        "analytic_line_ids.amount",
        "move_id",
        "move_id.state",
    )
    def _compute_distribution_done(self):
        for line in self:
            line.distribution_done = True
            if not line.move_id.state == "draft" and (
                line.account_id.analytic_template_ids or (line.analytic_account_id)
            ):
                line.distribution_done = False
                amount = round(sum(line.analytic_line_ids.mapped("amount")), 2)
                if amount != 0 and (
                    line.credit == abs(amount) or (line.debit == abs(amount))
                ):
                    line.distribution_done = True
            if line.distribution_done and any(
                [analitic.amount != 0 for (analitic) in line.analytic_line_ids]
            ):
                for analitic in line.analytic_line_ids.filtered(
                    lambda c: c.amount == 0
                ):
                    analitic.unlink()

    def action_show_distribution(self):
        """Returns an action that will open a form view (in a popup) allowing
        to work on all the analytic lines of a particular account move.
        """
        self.ensure_one()
        view = self.env.ref(
            "account_analytic_distribution.account_move_line_distribution_form_view"
        )
        return {
            "name": _("Distribution"),
            "type": "ir.actions.act_window",
            "view_mode": "form",
            "res_model": "account.move.line",
            "views": [(view.id, "form")],
            "view_id": view.id,
            "target": "new",
            "res_id": self.id,
            "context": self.env.context.copy(),
        }

    @api.constrains("analytic_line_ids", "debit", "credit")
    def _check_line_distribution(self):
        for line in self:
            if line.analytic_line_ids:
                amount = round(sum(line.analytic_line_ids.mapped("amount")), 2)
                if -amount != line.debit and (amount != line.credit) or (amount == 0):
                    raise ValidationError(
                        _(
                            "The total sum of amounts must be equal to the "
                            + "debit or credit amount of the financial movement."
                        )
                    )
