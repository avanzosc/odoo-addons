# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContractSubscriptionBase(TestContractBase):

    @classmethod
    def setUpClass(cls):
        super(TestContractSubscriptionBase, cls).setUpClass()
        cls.project = cls.env["project.project"].create({
            "name": "Test Subscription Project",
        })


class TestContractSubscription(TestContractSubscriptionBase):

    def test_invoice_creation_with_project(self):
        self.contract.invoice_project_id = self.project
        account_invoice_model = self.env['account.invoice']
        self.contract.recurring_create_invoice()
        invoice = account_invoice_model.search(
            [('contract_id', '=', self.contract.id)])
        for invoice_line in invoice.invoice_line_ids:
            self.assertEquals(invoice_line.account_analytic_id,
                              self.project.analytic_account_id)
            self.assertNotEquals(invoice_line.account_analytic_id,
                                 self.contract)

    def test_invoice_creation_without_project(self):
        account_invoice_model = self.env['account.invoice']
        self.contract.recurring_create_invoice()
        invoice = account_invoice_model.search(
            [('contract_id', '=', self.contract.id)])
        for invoice_line in invoice.invoice_line_ids:
            self.assertNotEquals(invoice_line.account_analytic_id,
                                 self.project.analytic_account_id)
            self.assertEquals(invoice_line.account_analytic_id,
                              self.contract)
