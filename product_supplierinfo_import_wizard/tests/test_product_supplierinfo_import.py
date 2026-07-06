import base64
import csv
from io import StringIO

from odoo import fields
from odoo.tests.common import TransactionCase


class TestProductSupplierinfoImport(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env["res.partner"]
        partner = Partner.search([("name", "=", "Test Supplier")], limit=1)
        if not partner:
            partner = Partner.search([], limit=1)
            partner.write({"name": "Test Supplier"})
        cls.supplier = partner
        cls.product_template = cls.env["product.template"].create(
            {
                "name": "Test Product",
                "default_code": "TST001",
                "company_id": cls.env.company.id,
            }
        )
        cls.currency_eur = cls.env.ref("base.EUR")

    def _create_wizard(self, values=None):
        vals = {
            "company_id": self.env.company.id,
        }
        if values:
            vals.update(values)
        return self.env["product.supplierinfo.import"].create(vals)

    def _create_wizard_with_csv(self, rows, fieldnames=None):
        if not fieldnames:
            fieldnames = [
                "Proveedor",
                "Plantilla de producto",
                "Código de producto",
                "Nombre del producto del proveedor",
                "Código de producto del proveedor",
                "Secuencia",
                "Moneda",
                "Cantidad mínima",
                "Fecha de inicio",
                "Fecha finalización",
                "Precio",
                "Tiempo inicial entrega",
            ]
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
        csv_content = output.getvalue()
        return self._create_wizard(
            {
                "data": base64.b64encode(csv_content.encode()),
                "filename": "test_import.csv",
            }
        )

    def _create_line(self, values=None):
        wizard = self._create_wizard()
        vals = {
            "import_id": wizard.id,
            "product_code": "TST001",
            "product_name": "Test Product",
            "supplier_name": "Test Supplier",
            "currency_code": "EUR",
            "price": 10.0,
            "min_qty": 1.0,
            "delay": 5,
            "sequence": 1,
        }
        if values:
            vals.update(values)
        line = self.env["product.supplierinfo.import.line"].create(vals)
        return line, wizard

    def _create_supplierinfo(self, values=None):
        vals = {
            "partner_id": self.supplier.id,
            "product_tmpl_id": self.product_template.id,
        }
        if values:
            vals.update(values)
        return self.env["product.supplierinfo"].create(vals)

    # === Wizard-level tests ===

    def test_get_line_values_full(self):
        wizard = self._create_wizard()
        row_values = {
            "Plantilla de producto": "Test Product",
            "Código de producto": "TST001",
            "Proveedor": "Test Supplier",
            "Nombre del producto del proveedor": "Vendor Name",
            "Código de producto del proveedor": "VENDOR001",
            "Secuencia": "5",
            "Moneda": "EUR",
            "Cantidad mínima": "2",
            "Fecha de inicio": "2024-01-01",
            "Fecha finalización": "2024-12-31",
            "Precio": "25.50",
            "Tiempo inicial entrega": "3",
        }
        result = wizard._get_line_values(row_values=row_values)
        self.assertEqual(result["product_code"], "TST001")
        self.assertEqual(result["product_name"], "Test Product")
        self.assertEqual(result["supplier_name"], "Test Supplier")
        self.assertEqual(result["supplier_product_name"], "Vendor Name")
        self.assertEqual(result["supplier_product_code"], "VENDOR001")
        self.assertEqual(result["sequence"], "5")
        self.assertEqual(result["currency_code"], "EUR")
        self.assertEqual(result["min_qty"], 2)
        self.assertEqual(result["price"], 25.50)
        self.assertEqual(result["delay"], 3)
        self.assertEqual(result["state"], "2validate")
        self.assertFalse(result["log_info"])

    def test_get_line_values_no_product(self):
        wizard = self._create_wizard()
        row_values = {
            "Plantilla de producto": "",
            "Código de producto": "",
            "Proveedor": "Test Supplier",
        }
        result = wizard._get_line_values(row_values=row_values)
        self.assertEqual(result, {})

    def test_get_line_values_code_only(self):
        wizard = self._create_wizard()
        row_values = {
            "Plantilla de producto": "",
            "Código de producto": "TST001",
            "Proveedor": "Test Supplier",
        }
        result = wizard._get_line_values(row_values=row_values)
        self.assertEqual(result["product_code"], "TST001")
        self.assertEqual(result["product_name"], "TST001")
        self.assertIn("Product Code added as Product Name", result["log_info"])
        self.assertEqual(result["state"], "error")

    def test_get_line_values_with_numeric_price(self):
        wizard = self._create_wizard()
        row_values = {
            "Plantilla de producto": "Test",
            "Código de producto": "TST002",
            "Proveedor": "Supplier",
            "Precio": 99.99,
        }
        result = wizard._get_line_values(row_values=row_values)
        self.assertEqual(result["price"], 99.99)

    def test_get_line_values_min_qty_zero(self):
        wizard = self._create_wizard()
        row_values = {
            "Plantilla de producto": "Test",
            "Código de producto": "TST003",
            "Proveedor": "Supplier",
            "Cantidad mínima": "0",
        }
        result = wizard._get_line_values(row_values=row_values)
        self.assertEqual(result["min_qty"], 0)

    def test_compute_supplierinfo_count(self):
        line1, wizard = self._create_line()
        self.env["product.supplierinfo.import.line"].create(
            {
                "import_id": wizard.id,
                "product_code": "TST002",
                "product_name": "Product 2",
                "supplier_name": "Supplier 2",
            }
        )
        wizard._compute_supplierinfo_count()
        self.assertEqual(wizard.supplierinfo_count, 0)
        line1.product_supplierinfo_id = self._create_supplierinfo()
        wizard._compute_supplierinfo_count()
        self.assertEqual(wizard.supplierinfo_count, 1)

    def test_button_open_import_line(self):
        wizard = self._create_wizard()
        action = wizard.button_open_import_line()
        self.assertIn("import_hide", action["context"])
        self.assertFalse(action["context"]["import_hide"])

    def test_button_open_supplierinfo(self):
        line, wizard = self._create_line()
        supplierinfo = self._create_supplierinfo()
        line.product_supplierinfo_id = supplierinfo
        action = wizard.button_open_supplierinfo()
        self.assertEqual(action["res_model"], "product.supplierinfo")
        self.assertIn(("id", "in", [supplierinfo.id]), action["domain"])

    def test_button_open_supplierinfo_no_supplierinfo(self):
        wizard = self._create_wizard()
        action = wizard.button_open_supplierinfo()
        self.assertEqual(action["res_model"], "product.supplierinfo")
        self.assertIn(("id", "in", []), action["domain"])

    def test_create_supplierinfo_with_extra_values(self):
        supplierinfo = self._create_supplierinfo({"price": 20.0, "min_qty": 5.0})
        self.assertTrue(supplierinfo.exists())
        self.assertEqual(supplierinfo.partner_id, self.supplier)
        self.assertEqual(supplierinfo.price, 20.0)
        self.assertEqual(supplierinfo.min_qty, 5.0)

    # === Import CSV flow ===

    def test_import_csv_file(self):
        rows = [
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Nombre del producto del proveedor": "Vendor Product",
                "Código de producto del proveedor": "VCODE001",
                "Secuencia": "10",
                "Moneda": "EUR",
                "Cantidad mínima": "1",
                "Fecha de inicio": "2024-01-01",
                "Fecha finalización": "2024-12-31",
                "Precio": "15.00",
                "Tiempo inicial entrega": "7",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        self.assertTrue(wizard.import_line_ids)
        self.assertEqual(len(wizard.import_line_ids), 1)
        line = wizard.import_line_ids[0]
        self.assertEqual(line.product_code, "TST001")
        self.assertEqual(line.product_name, "Test Product")
        self.assertEqual(line.supplier_name, "Test Supplier")
        self.assertEqual(line.currency_code, "EUR")
        self.assertEqual(line.price, 15.0)
        self.assertEqual(line.min_qty, 1)
        self.assertEqual(line.delay, 7)
        self.assertEqual(line.state, "2validate")

    def test_full_import_validate_process(self):
        rows = [
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Nombre del producto del proveedor": "Vendor Product",
                "Código de producto del proveedor": "VCODE001",
                "Secuencia": "10",
                "Moneda": "EUR",
                "Cantidad mínima": "1",
                "Fecha de inicio": "2024-01-01",
                "Fecha finalización": "2024-12-31",
                "Precio": "15.00",
                "Tiempo inicial entrega": "7",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        wizard.action_validate()
        line = wizard.import_line_ids[0]
        self.assertEqual(line.state, "pass")
        self.assertEqual(line.action, "create")
        self.assertEqual(line.supplier_id, self.supplier)
        self.assertEqual(line.product_tmpl_id, self.product_template)
        self.assertEqual(line.currency_id, self.currency_eur)
        wizard.action_process()
        self.assertEqual(line.state, "done")
        self.assertTrue(line.product_supplierinfo_id)
        supplierinfo = line.product_supplierinfo_id
        self.assertEqual(supplierinfo.partner_id, self.supplier)
        self.assertEqual(supplierinfo.product_tmpl_id, self.product_template)
        self.assertEqual(supplierinfo.min_qty, 1)
        self.assertEqual(supplierinfo.price, 15.0)
        self.assertEqual(supplierinfo.currency_id, self.currency_eur)
        self.assertEqual(supplierinfo.delay, 7)

    def test_import_validate_error_no_supplier(self):
        rows = [
            {
                "Proveedor": "Non Existent Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Moneda": "EUR",
                "Precio": "10.00",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        wizard.action_validate()
        line = wizard.import_line_ids[0]
        self.assertEqual(line.state, "error")
        self.assertIn("No supplier found", line.log_info)

    def test_import_validate_error_no_product(self):
        rows = [
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Non Existent Product",
                "Código de producto": "NONEXIST",
                "Moneda": "EUR",
                "Precio": "10.00",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        wizard.action_validate()
        line = wizard.import_line_ids[0]
        self.assertEqual(line.state, "error")
        self.assertIn("No product found", line.log_info)

    def test_import_validate_error_no_currency(self):
        rows = [
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Moneda": "__NONEXISTENT__",
                "Precio": "10.00",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        wizard.action_validate()
        line = wizard.import_line_ids[0]
        self.assertEqual(line.state, "error")
        self.assertIn("No currency found", line.log_info)

    def test_import_multiple_lines(self):
        rows = [
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Moneda": "EUR",
                "Precio": "10.00",
            },
            {
                "Proveedor": "Test Supplier",
                "Plantilla de producto": "Test Product",
                "Código de producto": "TST001",
                "Moneda": "EUR",
                "Precio": "20.00",
            },
        ]
        wizard = self._create_wizard_with_csv(rows)
        wizard.action_import_file()
        self.assertEqual(len(wizard.import_line_ids), 2)
        wizard.action_validate()
        for line in wizard.import_line_ids:
            self.assertEqual(line.state, "pass")
        wizard.action_process()
        for line in wizard.import_line_ids:
            self.assertEqual(line.state, "done")
            self.assertTrue(line.product_supplierinfo_id)

    # === Line-level tests ===

    def test_onchange_product_tmpl_id(self):
        line, _wizard = self._create_line(
            {"product_name": False, "product_code": False}
        )
        self.assertFalse(line.product_name)
        self.assertFalse(line.product_code)
        line.product_tmpl_id = self.product_template
        line.onchange_product_tmpl_id()
        self.assertEqual(line.product_name, "Test Product")
        self.assertEqual(line.product_code, "TST001")

    def test_onchange_supplier_id(self):
        line, _wizard = self._create_line()
        line.supplier_id = self.supplier
        line.onchange_supplier_id()
        self.assertEqual(line.supplier_name, "Test Supplier")

    def test_check_supplier_already_set(self):
        line, _wizard = self._create_line({"supplier_id": self.supplier.id})
        supplier, log_info = line._check_supplier()
        self.assertEqual(supplier, self.supplier)
        self.assertFalse(log_info)

    def test_check_supplier_found(self):
        line, _wizard = self._create_line()
        supplier, log_info = line._check_supplier()
        self.assertEqual(supplier, self.supplier)
        self.assertFalse(log_info)

    def test_check_supplier_not_found(self):
        line, _wizard = self._create_line({"supplier_name": "Non Existent Supplier"})
        supplier, log_info = line._check_supplier()
        self.assertFalse(supplier)
        self.assertIn("No supplier found", log_info)

    def test_check_supplier_multiple(self):
        partners = self.env["res.partner"].search([("parent_id", "=", False)], limit=2)
        partners.write({"name": "Test Supplier"})
        line, _wizard = self._create_line()
        supplier, log_info = line._check_supplier()
        self.assertFalse(supplier)
        self.assertIn("More than one supplier", log_info)

    def test_check_product_already_set(self):
        line, _wizard = self._create_line({"product_tmpl_id": self.product_template.id})
        product, log_info = line._check_product()
        self.assertEqual(product, self.product_template)
        self.assertFalse(log_info)

    def test_check_product_found_by_code(self):
        line, _wizard = self._create_line()
        product, log_info = line._check_product()
        self.assertEqual(product, self.product_template)
        self.assertFalse(log_info)

    def test_check_product_found_by_barcode(self):
        self.product_template.barcode = "BARCODE001"
        line, _wizard = self._create_line(
            {
                "product_code": False,
                "product_barcode": "BARCODE001",
            }
        )
        product, log_info = line._check_product()
        self.assertEqual(product, self.product_template)
        self.assertFalse(log_info)

    def test_check_product_not_found(self):
        line, _wizard = self._create_line(
            {
                "product_code": "NONEXIST",
                "product_name": "No Product Here",
            }
        )
        product, log_info = line._check_product()
        self.assertFalse(product)
        self.assertIn("No product found", log_info)

    def test_check_product_multiple(self):
        self.env["product.template"].create(
            {
                "name": "Test Product",
                "default_code": "TST001",
                "company_id": self.env.company.id,
            }
        )
        line, _wizard = self._create_line()
        product, log_info = line._check_product()
        self.assertFalse(product)
        self.assertIn("More than one product", log_info)

    def test_check_currency_already_set(self):
        line, _wizard = self._create_line({"currency_id": self.currency_eur.id})
        currency, log_info = line._check_currency()
        self.assertEqual(currency, self.currency_eur)
        self.assertFalse(log_info)

    def test_check_currency_found(self):
        line, _wizard = self._create_line()
        currency, log_info = line._check_currency()
        self.assertEqual(currency, self.currency_eur)
        self.assertFalse(log_info)

    def test_check_currency_not_found(self):
        line, _wizard = self._create_line({"currency_code": "__NONEXISTENT__"})
        currency, log_info = line._check_currency()
        self.assertFalse(currency)
        self.assertIn("No currency found", log_info)

    def test_check_currency_inactive(self):
        inactive_currency = self.env["res.currency"].create(
            {
                "name": "TST",
                "symbol": "T",
                "currency_unit_label": "Test",
                "currency_subunit_label": "Test sub",
                "active": False,
            }
        )
        line, _wizard = self._create_line({"currency_code": "TST"})
        currency, log_info = line._check_currency()
        self.assertEqual(currency, inactive_currency)
        self.assertIn("'TST' is inactive.", log_info)

    def test_action_validate_success(self):
        line, _wizard = self._create_line(
            {
                "supplier_id": self.supplier.id,
                "product_tmpl_id": self.product_template.id,
                "currency_id": self.currency_eur.id,
            }
        )
        result = line._action_validate()
        self.assertEqual(result["state"], "pass")
        self.assertEqual(result["action"], "create")
        self.assertEqual(result["supplier_id"], self.supplier.id)
        self.assertEqual(result["product_tmpl_id"], self.product_template.id)
        self.assertEqual(result["currency_id"], self.currency_eur.id)

    def test_action_validate_failure(self):
        line, _wizard = self._create_line(
            {
                "supplier_name": "Non Existent",
                "product_code": "NONEXIST",
                "product_name": "Non Existent Product Name",
                "currency_code": "__NONEXISTENT__",
            }
        )
        result = line._action_validate()
        self.assertEqual(result["state"], "error")
        self.assertEqual(result["action"], "nothing")
        self.assertIn("No supplier found", result["log_info"])
        self.assertIn("No product found", result["log_info"])
        self.assertIn("No currency found", result["log_info"])

    def test_action_process(self):
        line, _wizard = self._create_line(
            {
                "supplier_id": self.supplier.id,
                "product_tmpl_id": self.product_template.id,
                "currency_id": self.currency_eur.id,
                "price": 15.0,
                "min_qty": 2.0,
                "delay": 3,
                "sequence": 5,
            }
        )
        result = line._action_process()
        self.assertEqual(result["state"], "done")
        self.assertEqual(result["log_info"], "")
        self.assertTrue(result["product_supplierinfo_id"])
        supplierinfo = self.env["product.supplierinfo"].browse(
            result["product_supplierinfo_id"]
        )
        self.assertTrue(supplierinfo.exists())
        self.assertEqual(supplierinfo.partner_id, self.supplier)
        self.assertEqual(supplierinfo.product_tmpl_id, self.product_template)
        self.assertEqual(supplierinfo.currency_id, self.currency_eur)
        self.assertEqual(supplierinfo.price, 15.0)
        self.assertEqual(supplierinfo.min_qty, 2.0)
        self.assertEqual(supplierinfo.delay, 3)
        self.assertEqual(supplierinfo.sequence, 5)

    def test_product_supplierinfo_values(self):
        line, _wizard = self._create_line(
            {
                "supplier_id": self.supplier.id,
                "product_tmpl_id": self.product_template.id,
                "currency_id": self.currency_eur.id,
                "price": 25.0,
                "min_qty": 3.0,
                "delay": 10,
                "sequence": 2,
                "date_start": "2024-06-01",
                "date_end": "2024-12-31",
            }
        )
        values = line._product_supplierinfo_values()
        self.assertEqual(values["partner_id"], self.supplier.id)
        self.assertEqual(values["product_tmpl_id"], self.product_template.id)
        self.assertEqual(values["min_qty"], 3.0)
        self.assertEqual(values["price"], 25.0)
        self.assertEqual(values["currency_id"], self.currency_eur.id)
        self.assertEqual(values["delay"], 10)
        self.assertEqual(values["sequence"], 2)
        self.assertEqual(values["date_start"], fields.Date.to_date("2024-06-01"))
        self.assertEqual(values["date_end"], fields.Date.to_date("2024-12-31"))

    def test_state_computation(self):
        wizard = self._create_wizard()
        self.assertEqual(wizard.state, "draft")
        line, _wizard = self._create_line({"import_id": wizard.id})
        wizard._compute_state()
        self.assertEqual(wizard.state, "2validate")
        line.write({"state": "pass"})
        wizard._compute_state()
        self.assertEqual(wizard.state, "pass")
        line.write({"state": "done"})
        wizard._compute_state()
        self.assertEqual(wizard.state, "done")
        line2 = self.env["product.supplierinfo.import.line"].create(
            {
                "import_id": wizard.id,
                "product_code": "TST002",
                "product_name": "Product 2",
            }
        )
        line2.write({"state": "error"})
        wizard._compute_state()
        self.assertEqual(wizard.state, "error")
