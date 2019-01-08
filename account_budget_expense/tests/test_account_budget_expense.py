# Copyright 2019 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestAccountBudgetExpense(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountBudgetExpense, cls).setUpClass()
        cls.position_model = cls.env['account.budget.post']
        cls.position = cls.position_model.create({
            'name': 'Test Project',
            'account_ids': [
                (4, x.id) for x in cls.env['account.account'].search(
                    [('deprecated', '=', False)], limit=1)],
        })

    def test_change_expense_check(self):
        self.assertFalse(self.position.expenses)
        self.position.expenses = True
        self.assertTrue(self.position.expenses)

    def test_copy_expense_check(self):
        self.position.expenses = True
        self.assertTrue(self.position.expenses)
        new_position = self.position.copy()
        self.assertFalse(new_position.expenses)

    def test_new_expense_check(self):
        expenses = self.position_model.search([('expenses', '=', True)])
        self.assertFalse(expenses)
        self.position_model.create({
            'name': 'New Expenses Position',
            'expenses': True,
            'account_ids': [
                (4, x.id) for x in self.env['account.account'].search(
                    [('deprecated', '=', False)], limit=1)],

        })
        expenses = self.position_model.search([('expenses', '=', True)])
        self.assertTrue(expenses)

    def test_new_expense_check_exception(self):
        self.position.expenses = True
        self.assertTrue(self.position.expenses)
        with self.assertRaises(ValidationError):
            self.position_model.create({
                'name': 'New Expenses Position',
                'expenses': True,
                'account_ids': [
                    (4, x.id) for x in self.env['account.account'].search(
                        [('deprecated', '=', False)], limit=1)],

            })
