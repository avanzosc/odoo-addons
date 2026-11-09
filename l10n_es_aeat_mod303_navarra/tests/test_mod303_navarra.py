# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

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
