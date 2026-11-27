from unittest.mock import MagicMock

from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestProductVariantStockReportXlsx(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.report = cls.env["report.stock.product_xlsx"]
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Variant",
                "default_code": "TEST-VARIANT",
                "type": "consu",
                "is_storable": True,
            }
        )
        cls.warehouse = cls.env["stock.warehouse"].search(
            [("company_id", "=", cls.company.id)], limit=1
        )
        cls.orderpoint = cls.env["stock.warehouse.orderpoint"].create(
            {
                "name": "Test Orderpoint Main",
                "product_id": cls.product.id,
                "warehouse_id": cls.warehouse.id,
                "location_id": cls.warehouse.lot_stock_id.id,
                "company_id": cls.company.id,
                "product_min_qty": 1.0,
                "product_max_qty": 5.0,
                "qty_multiple": 2.0,
            }
        )
        partner = cls.env["res.partner"].create({"name": "Test Vendor"})
        cls.env["product.supplierinfo"].create(
            {
                "partner_id": partner.id,
                "product_tmpl_id": cls.product.product_tmpl_id.id,
                "product_id": cls.product.id,
                "min_qty": 2.0,
                "price": 12.5,
                "currency_id": cls.company.currency_id.id,
            }
        )

    def _written_value(self, workbook, row, column):
        worksheet = workbook.add_worksheet.return_value
        for call in worksheet.write.call_args_list:
            if call.args[:2] == (row, column):
                return call.args[2]
        return None

    def test_report_headers_and_company_orderpoint(self):
        other_company = self.env["res.company"].create(
            {"name": "Other Company", "currency_id": self.company.currency_id.id}
        )
        other_warehouse = self.env["stock.warehouse"].create(
            {
                "name": "Other Warehouse",
                "code": "OWH",
                "company_id": other_company.id,
            }
        )
        self.env["stock.warehouse.orderpoint"].create(
            {
                "name": "Test Orderpoint Other",
                "product_id": self.product.id,
                "warehouse_id": other_warehouse.id,
                "location_id": other_warehouse.lot_stock_id.id,
                "company_id": other_company.id,
                "product_min_qty": 10.0,
                "product_max_qty": 50.0,
                "qty_multiple": 20.0,
            }
        )
        workbook = MagicMock()
        self.report.generate_xlsx_report(
            workbook, {"force_company_id": self.company.id}, self.product
        )

        self.assertEqual(self._written_value(workbook, 1, 6), "Sales")
        self.assertEqual(self._written_value(workbook, 1, 7), "Purchase")
        self.assertEqual(self._written_value(workbook, 2, 6), self.product.sale_ok)
        self.assertEqual(self._written_value(workbook, 2, 7), self.product.purchase_ok)
        self.assertEqual(self._written_value(workbook, 2, 24), 1.0)
        self.assertEqual(self._written_value(workbook, 2, 25), 5.0)
        self.assertEqual(self._written_value(workbook, 2, 26), 2.0)
        self.assertEqual(
            self._written_value(workbook, 2, 27), self.orderpoint.days_to_order
        )

    def test_report_vendor_and_serie_columns(self):
        workbook = MagicMock()
        self.report.generate_xlsx_report(
            workbook, {"force_company_id": self.company.id}, self.product
        )
        vendor_detail = self._written_value(workbook, 2, 20)

        self.assertEqual(self._written_value(workbook, 1, 13), "Serie")
        self.assertIsInstance(self._written_value(workbook, 2, 13), str)
        self.assertIn("Test Vendor", vendor_detail)
        self.assertIn("2*12.5", vendor_detail)
        self.assertNotIn("{vendor", vendor_detail)

    def test_report_account_columns_match_header(self):
        workbook = MagicMock()
        self.report.generate_xlsx_report(
            workbook, {"force_company_id": self.company.id}, self.product
        )
        accounts = self.product.with_company(self.company)._get_product_accounts()
        expected_expense = accounts.get("expense")
        expected_income = accounts.get("income")

        self.assertEqual(
            self._written_value(workbook, 2, 14),
            expected_expense and expected_expense.code or "",
        )
        self.assertEqual(
            self._written_value(workbook, 2, 15),
            expected_income and expected_income.code or "",
        )

    def test_wizard_resets_subfamily_when_family_changes(self):
        family = self.env["product.category"].create({"name": "Family"})
        other_family = self.env["product.category"].create({"name": "Other Family"})
        subfamily = self.env["product.category"].create(
            {"name": "Subfamily", "parent_id": family.id}
        )
        wizard = self.env["report.stock.product_xlsx.export"].create(
            {
                "company_id": self.company.id,
                "family_id": family.id,
                "sub_family_id": subfamily.id,
            }
        )

        wizard.family_id = other_family
        wizard._onchange_family_id()

        self.assertFalse(wizard.sub_family_id)
