# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    payment_reference = fields.Char(related="move_id.payment_reference")
    distribution_done = fields.Boolean(compute="_compute_distribution_done", store=True)
    account_name = fields.Char(compute="_compute_account_name")

    @api.depends("account_id")
    def _compute_account_name(self):
        for line in self:
            line.account_name = line.account_id.display_name or ""

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
            rounding = line.currency_id.rounding or line.company_currency_id.rounding
            line.distribution_done = True
            if not line.move_id.state == "draft" and (
                line.account_id.analytic_template_ids or line.analytic_distribution
            ):
                line.distribution_done = False
                amount = sum(line.analytic_line_ids.mapped("amount"))
                if not float_is_zero(amount, precision_rounding=rounding) and (
                    float_compare(line.credit, abs(amount), precision_rounding=rounding)
                    == 0
                    or float_compare(
                        line.debit, abs(amount), precision_rounding=rounding
                    )
                    == 0
                ):
                    line.distribution_done = True
            if line.distribution_done and any(
                not float_is_zero(analytic.amount, precision_rounding=rounding)
                for analytic in line.analytic_line_ids
            ):
                for analytic in line.analytic_line_ids.filtered(
                    lambda c: c.amount == 0
                ):
                    analytic.unlink()

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
                rounding = (
                    line.currency_id.rounding or line.company_currency_id.rounding
                )
                amount = sum(line.analytic_line_ids.mapped("amount"))
                invalid_distribution = (
                    float_compare(-amount, line.debit, precision_rounding=rounding) != 0
                    and float_compare(amount, line.credit, precision_rounding=rounding)
                    != 0
                ) or float_is_zero(amount, precision_rounding=rounding)
                if invalid_distribution:
                    raise ValidationError(
                        _(
                            "The total sum of amounts must be equal to the "
                            + "debit or credit amount of the financial movement."
                        )
                    )
