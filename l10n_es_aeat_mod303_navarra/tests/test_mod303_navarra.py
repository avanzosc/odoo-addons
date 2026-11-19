# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

import base64

from odoo import exceptions

from odoo.addons.l10n_es_aeat_mod303.tests.test_l10n_es_aeat_mod303 import (
    TestL10nEsAeatMod303Base,
)


class TestL10nEsAeatMod303Navarra(TestL10nEsAeatMod303Base):
    taxes_sale = {"S_IVA21B": (100, 21)}
    taxes_purchase = {"P_IVA21_BC": (1000, 210)}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.navarra_agency = cls.env.ref("l10n_es_aeat.aeat_tax_agency_navarra")
        cls.company.write({"tax_agency_id": cls.navarra_agency.id})
        cls.model303_4t.write({"navarra_cifra_relativa": 90.0})

    def _create_report(self, year, period_type, date_start, date_end):
        return self.env["l10n.es.aeat.mod303.report"].create(
            {
                "company_id": self.company.id,
                "company_vat": "1234567890",
                "contact_name": "Test owner",
                "statement_type": "N",
                "support_type": "T",
                "contact_phone": "911234455",
                "year": year,
                "period_type": period_type,
                "date_start": date_start,
                "date_end": date_end,
                "journal_id": self.journal_misc.id,
            }
        )

    def test_navarra_casillas_y_compensacion(self):
        self._invoice_sale_create("2024-11-01")
        self._invoice_purchase_create("2024-11-01")
        self.model303_4t.button_calculate()
        self.assertAlmostEqual(self.model303_4t.navarra_casilla_50, 210.0, 2)
        self.assertAlmostEqual(self.model303_4t.navarra_casilla_61, -170.1, 2)
        self.assertAlmostEqual(self.model303_4t.navarra_casilla_63, -170.1, 2)
        self.model303_4t.navarra_compensar = True

        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        self.assertAlmostEqual(report_1t_2025.navarra_cifra_relativa, 90.0, 4)
        report_1t_2025.button_calculate()
        self.assertAlmostEqual(report_1t_2025.navarra_casilla_50, 0.0, 2)
        self.assertAlmostEqual(report_1t_2025.navarra_casilla_61, 0.0, 2)
        self.assertAlmostEqual(report_1t_2025.navarra_casilla_62, 170.1, 2)
        self.assertAlmostEqual(report_1t_2025.navarra_casilla_63, -170.1, 2)

    def test_navarra_cifra_relativa_tres_primeros_trimestres(self):
        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        self.assertAlmostEqual(report_1t_2025.navarra_cifra_relativa, 90.0, 4)
        with self.assertRaises(exceptions.ValidationError):
            report_1t_2025.navarra_cifra_relativa = 80.0

    def test_navarra_modo_pago(self):
        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        report_1t_2025.button_calculate()
        with self.assertRaises(exceptions.ValidationError):
            report_1t_2025.navarra_modo_pago = "1"

    def test_navarra_resumen_anual(self):
        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        with self.assertRaises(exceptions.ValidationError):
            report_1t_2025.navarra_casilla_164 = True
        with self.assertRaises(exceptions.ValidationError):
            self.model303_4t.navarra_casilla_164 = True
            self.model303_4t.navarra_casilla_165 = True

    def test_navarra_exentas(self):
        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        with self.assertRaises(exceptions.ValidationError):
            report_1t_2025.navarra_casilla_264 = True
            report_1t_2025.navarra_casilla_265 = True

    def _export_records(self, report):
        report.button_navarra_export()
        content = base64.b64decode(report.navarra_export_file).decode("latin-1")
        records = content.splitlines()
        self.assertTrue(records)
        for record in records:
            self.assertEqual(len(record), 250)
        return records

    def _export_casillas(self, records):
        casillas = {}
        for record in records:
            if record[0] != "2":
                continue
            for index in range(10):
                slot = record[26 + index * 20 : 46 + index * 20]
                if not slot.strip():
                    continue
                code = int(slot[:4])
                value = int(slot[5:])
                decimals = 4 if code == 55 else 2
                if code in (93, 164, 165, 264, 265):
                    decimals = 0
                amount = value / (10**decimals)
                casillas[code] = -amount if slot[4] == "N" else amount
        return casillas

    def test_navarra_export_f66(self):
        report_12_2024 = self._create_report(2024, "12", "2024-12-01", "2024-12-31")
        report_12_2024.navarra_cifra_relativa = 90.0
        self._invoice_sale_create("2024-12-01")
        self._invoice_purchase_create("2024-12-01")
        report_12_2024.button_calculate()
        records = self._export_records(report_12_2024)
        self.assertTrue(records[0].startswith("0F66"))
        self.assertTrue(records[1].startswith("1F66"))
        self.assertEqual(records[1][8:11], "412")
        self.assertEqual(int(records[0][109:117]), 1)
        self.assertEqual(
            int(records[0][117:125]),
            len([record for record in records if record[0] == "2"]),
        )
        casillas = self._export_casillas(records)
        self.assertAlmostEqual(casillas[3], 100.0, 2)
        self.assertAlmostEqual(casillas[13], 21.0, 2)
        self.assertAlmostEqual(casillas[20], 21.0, 2)
        self.assertAlmostEqual(casillas[31], 1000.0, 2)
        self.assertAlmostEqual(casillas[41], 210.0, 2)
        self.assertAlmostEqual(casillas[50], 210.0, 2)
        self.assertAlmostEqual(casillas[55], 90.0, 4)
        self.assertAlmostEqual(casillas[61], -170.1, 2)
        self.assertAlmostEqual(casillas[63], -170.1, 2)
        self.assertAlmostEqual(casillas[64], 170.1, 2)
        self.assertNotIn(70, casillas)
        self.assertAlmostEqual(casillas[110], 21.0, 2)
        self.assertAlmostEqual(casillas[111], 210.0, 2)
        self.assertAlmostEqual(casillas[112], -189.0, 2)

    def test_navarra_export_f69(self):
        report_1t_2025 = self._create_report(2025, "1T", "2025-01-01", "2025-03-31")
        report_1t_2025.contact_email = "test@example.com"
        report_1t_2025.button_calculate()
        records = self._export_records(report_1t_2025)
        self.assertTrue(records[0].startswith("0F69"))
        self.assertTrue(records[1].startswith("1F69"))
        self.assertEqual(records[1][8:11], "100")
        record3 = [record for record in records if record.startswith("3F69")]
        self.assertEqual(len(record3), 1)
        self.assertIn("3003test@example.com", record3[0])
        casillas = self._export_casillas(records)
        self.assertAlmostEqual(casillas[20], 0.0, 2)
        self.assertAlmostEqual(casillas[50], 0.0, 2)
        self.assertAlmostEqual(casillas[55], 90.0, 4)
        self.assertAlmostEqual(casillas[61], 0.0, 2)
        self.assertAlmostEqual(casillas[63], 0.0, 2)
        self.assertNotIn(64, casillas)
        self.assertNotIn(70, casillas)
        self.assertNotIn(110, casillas)

    def test_navarra_export_compensar(self):
        self._invoice_purchase_create("2024-11-01")
        self.model303_4t.button_calculate()
        self.model303_4t.navarra_compensar = True
        records = self._export_records(self.model303_4t)
        casillas = self._export_casillas(records)
        self.assertAlmostEqual(casillas[70], 189.0, 2)
        self.assertNotIn(64, casillas)
