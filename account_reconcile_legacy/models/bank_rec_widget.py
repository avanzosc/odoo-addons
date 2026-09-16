# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class BankRecWidget(models.Model):
    _inherit = "bank.rec.widget"

    def _lines_check_apply_early_payment_discount(
        self,
    ):
        if self.env.context.get("legacy_bank_rec_no_auto_adjust"):
            return False

        return super()._lines_check_apply_early_payment_discount()

    def _lines_check_apply_partial_matching(
        self,
    ):
        if self.env.context.get("legacy_bank_rec_no_auto_adjust"):
            return False

        return super()._lines_check_apply_partial_matching()

    def _js_action_add_new_aml_legacy(
        self,
        aml_id,
    ):
        self.ensure_one()

        aml = self.env["account.move.line"].browse(aml_id)

        self.with_context(legacy_bank_rec_no_auto_adjust=True)._action_add_new_amls(
            aml,
            allow_partial=False,
        )

    def _js_action_remove_new_aml_legacy(
        self,
        aml_id,
    ):
        self.ensure_one()

        aml = self.env["account.move.line"].browse(aml_id)

        self.with_context(legacy_bank_rec_no_auto_adjust=True)._action_remove_new_amls(
            aml
        )

    def _js_action_remove_line_legacy(
        self,
        line_index,
    ):
        self.ensure_one()

        line = self.line_ids.filtered(lambda x: x.index == line_index)

        self.with_context(legacy_bank_rec_no_auto_adjust=True)._action_remove_lines(
            line
        )
