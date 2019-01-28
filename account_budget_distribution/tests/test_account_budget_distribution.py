# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.addons.account_budget.tests.common import TestAccountBudgetCommon


class TestAccountBudgetDistribution(TestAccountBudgetCommon):

    def test_account_budget_distribution(self):
        pessimistic_budget = self.browse_ref(
            'account_budget.crossovered_budget_budgetpessimistic0')
        self.assertTrue(pessimistic_budget.summary_ids)
        pessimistic_summary = pessimistic_budget.summary_ids
        wizard = self.env['crossovered.budget.distribution'].with_context(
            active_model=pessimistic_budget._name,
            active_id=pessimistic_budget.id).create({})
        self.assertEquals(len(wizard.line_ids), len(pessimistic_summary))
        planned_amounts = {}
        for line in wizard.line_ids:
            self.assertEquals(
                line.planned_amount, pessimistic_summary.filtered(
                    lambda s: s.general_budget_id == line.budget_post_id
                ).planned_amount)
            budget_lines = pessimistic_budget.crossovered_budget_line.filtered(
                lambda l: l.general_budget_id == line.budget_post_id)
            try:
                budget_lines = budget_lines.filtered(
                    lambda l: not l.general_budget_id.expenses)
            except Exception:
                pass
            if budget_lines:
                planned_amounts.update({
                    line.budget_post_id.id: (
                        line.planned_amount / len(budget_lines)),
                })
        wizard.button_distribute_amount()
        budget_lines = pessimistic_budget.crossovered_budget_line
        try:
            budget_lines = budget_lines.filtered(
                lambda l: not l.general_budget_id.expenses)
        except Exception:
            pass
        for budget_line in budget_lines:
            self.assertEquals(
                budget_line.planned_amount,
                planned_amounts[budget_line.general_budget_id.id])
