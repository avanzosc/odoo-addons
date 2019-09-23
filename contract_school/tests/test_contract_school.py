# Copyright 2019 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common
from odoo import fields
from dateutil.relativedelta import relativedelta


@common.at_install(False)
@common.post_install(True)
class TestContractSchool(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestContractSchool, cls).setUpClass()
        cls.product_model = cls.env['product.product']
        cls.account_model = cls.env['contract.contract']
        cls.line_model = cls.env['contract.line']
        cls.partner_model = cls.env['res.partner']
        cls.invoice_model = cls.env['account.invoice']
        today = fields.Date.from_string(fields.Date.today())
        start = today + relativedelta(months=-1)
        end = today + relativedelta(months=+1)
        family_vals = {
            'name': 'Family for test sale_crm_school',
            'educational_category': 'family',
        }
        cls.family = cls.partner_model.create(family_vals)
        cls.product = cls.product_model.search([], limit=1)
        account_vals = {
            'name': 'Contract for test contract_school',
            'partner_id': cls.family.id,
            'contract_type': 'sale',
        }
        cls.account = cls.account_model.create(account_vals)
        line_vals = {
            'contract_id': cls.account.id,
            'product_id': cls.product.id,
            'name': cls.product.name,
            'uom_id': cls.product.uom_id.id,
            'recurring_next_date': today,
            'date_start': start,
            'date_end': end,
        }
        cls.line = cls.line_model.create(line_vals)
        cls.line._onchange_product_id()
        cls.line.write({
            'price_unit': 800,
            'payment_percentage': 50.0,
        })
        cls.line2 = cls.line.copy()
        cls.line2._onchange_product_id()
        cls.line2.write({
            'price_unit': 200,
            'payment_percentage': 100.0,
            'recurring_next_date': start,
            'date_end': start,
        })
        cls.line3 = cls.line.copy()
        cls.line3._onchange_product_id()
        cls.line3.write({
            'price_unit': 300,
            'payment_percentage': 100.0,
            'recurring_next_date': end,
        })

    def test_contract_school(self):
        for line in self.account.contract_line_ids:
            subtotal = line.quantity * line.price_unit
            discount = line.discount / 100
            subtotal *= 1 - discount
            subtotal *= line.payment_percentage / 100
            self.assertEquals(line.price_subtotal, subtotal)
        self.account_model.cron_recurring_create_invoice()
        invoices = self.account._get_related_invoices()
        self.assertEquals(len(invoices), 1)
        self.assertEquals(len(invoices[0].invoice_line_ids), 2)
        self.assertEquals(
            invoices[0].invoice_line_ids[0].payment_percentage, 50.0)
        self.assertEquals(
            invoices[0].invoice_line_ids[0].price_subtotal, 400.0)
