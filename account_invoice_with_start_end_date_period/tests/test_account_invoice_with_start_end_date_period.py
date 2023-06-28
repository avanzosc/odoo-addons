# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from dateutil.relativedelta import relativedelta
from odoo import fields
from odoo.tests import common, tagged


@tagged("post_install", "-at_install")
class TestAccountInvoiceWithStartEndDatePeriod(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountInvoiceWithStartEndDatePeriod, cls).setUpClass()
        cls.product_obj = cls.env["product.product"]
        cls.sale_obj = cls.env["sale.order"]
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
        sale_line_vals = {
            "product_id": cls.product.id,
            "name": cls.product.name,
            "product_uom_qty": 1,
            "product_uom": cls.product.uom_id.id,
            "price_unit": 100,
        }
        sale_vals = {
            "partner_id": cls.customer.id,
            "partner_invoice_id": cls.customer.id,
            "partner_shipping_id": cls.customer.id,
            "company_id": cls.company.id,
            "order_line": [(0, 0, sale_line_vals)],
        }
        cls.sale = cls.sale_obj.create(sale_vals)

    def test_account_invoice_with_start_end_date_period(self):
        self.sale.action_confirm()
        self.sale._create_invoices(
            start_date=fields.Date.today(),
            end_date=fields.Date.today() + relativedelta(days=+7),
        )
        self.assertEqual(
            self.sale.invoice_ids[0].start_date_period, fields.Date.today()
        )
        self.assertEqual(
            self.sale.invoice_ids[0].end_date_period,
            fields.Date.today() + relativedelta(days=+7),
        )
