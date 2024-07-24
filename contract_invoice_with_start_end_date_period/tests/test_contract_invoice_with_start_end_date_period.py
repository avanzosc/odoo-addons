# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestContractInvoiceWithStartEndDatePeriod(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestContractInvoiceWithStartEndDatePeriod, cls).setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.contract_obj = cls.env["contract.contract"]
        cls.uom_unit = cls.env.ref("uom.product_uom_unit")
        cls.company = cls.env["res.company"]._company_default_get("sale.order")
        cls.product = cls.product_obj.create(
            {
                "name": "product account invoice with start end date period",
                "default_code": "PAIWSEDP",
                "uom_id": cls.uom_unit.id,
                "uom_po_id": cls.uom_unit.id,
                "type": "service",
                "invoice_policy": "order",
            }
        )
        cls.customer = cls.env.ref("base.res_partner_12")
        contract_line_vals = {
            "product_id": cls.product.id,
            "name": cls.product.name,
            "uom_id": cls.product.uom_id.id,
            "quantity": 1,
            "price_unit": 500,
        }
        contract_vals = {
            "name": "Contract account invoice with start end date period",
            "partner_id": cls.customer.id,
            "line_recurrence": True,
            "contract_line_ids": [(0, 0, contract_line_vals)],
        }
        cls.contract = cls.contract_obj.create(contract_vals)

    def test_contract_invoice_with_start_end_date_period(self):
        start_date = self.contract.contract_line_ids[0].next_period_date_start
        end_date = self.contract.contract_line_ids[0].next_period_date_end
        self.contract.recurring_create_invoice()
        invoice = self.contract._get_related_invoices()
        self.assertEqual(invoice.start_date_period, start_date)
        self.assertEqual(invoice.end_date_period, end_date)
