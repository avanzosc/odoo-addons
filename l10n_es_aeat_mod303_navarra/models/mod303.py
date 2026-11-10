# Copyright 2026 AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
"""Casillas navarras del F66/F69 integradas en el modelo 303.

El modelo 303 de OCA sigue siendo la declaración estatal. Este módulo añade,
sin alterar la exportación oficial del 303, las casillas específicas que la
Hacienda Foral de Navarra utiliza en su modelo F66/F69:

* [55] Cifra relativa.
* [50] IVA deducible.
* [61] Cuota resultante.
* [62] Cuota a compensar de periodos anteriores.
* [63] Resultado final.
* [69] Regularización anual (mapeada sobre la casilla 68 del 303).
* Modo de pago.
* [93] Sin actividad.
* [164]/[165] Resumen anual de operaciones.
* [264]/[265] Operaciones exentas sin derecho a deducción.

También genera los ficheros de presentación F66/F69 de la Hacienda Foral de
Navarra a partir de los datos del modelo 303.
"""

import base64
import re
import unicodedata
from decimal import ROUND_HALF_UP, Decimal

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare

NAVARRA_F66_PERIODS = tuple(f"{month:02d}" for month in range(1, 13))
NAVARRA_F69_PERIODS = ("1T", "2T", "3T", "4T")
NAVARRA_LAST_PERIODS = ("4T", "12")

NAVARRA_CASILLA_ORDER = (
    93,
    264,
    265,
    266,
    267,
    10,
    1,
    2,
    23,
    194,
    171,
    3,
    13,
    4,
    14,
    5,
    15,
    6,
    16,
    51,
    52,
    7,
    17,
    8,
    18,
    9,
    19,
    172,
    173,
    176,
    177,
    20,
    31,
    41,
    131,
    141,
    32,
    42,
    39,
    49,
    170,
    43,
    174,
    175,
    178,
    179,
    45,
    450,
    47,
    48,
    50,
    55,
    61,
    62,
    69,
    63,
    64,
    70,
    104,
    105,
    106,
    107,
    108,
    109,
    1014,
    110,
    111,
    112,
    901,
    902,
    903,
    904,
    905,
    906,
    907,
    908,
    909,
    910,
    952,
    953,
    911,
    912,
    913,
    914,
    915,
    916,
    917,
    918,
    950,
    948,
    949,
    951,
    919,
    920,
    921,
    922,
    923,
    924,
    925,
    926,
    927,
    928,
    960,
    961,
    933,
    934,
    213,
    935,
    936,
    937,
    938,
    941,
    942,
    215,
    203,
    216,
    204,
    214,
    954,
    966,
    967,
    968,
    217,
    305,
    307,
    303,
    195,
    196,
    197,
)

NAVARRA_ZERO_DECIMAL_CASILLAS = {
    93,
    164,
    165,
    264,
    265,
    266,
    267,
    303,
    305,
    307,
    1014,
}
NAVARRA_ALWAYS_CASILLAS = {20, 50, 55, 61, 62, 63, 69}
NAVARRA_MARKER_CASILLAS = {
    93,
    164,
    165,
    264,
    265,
    266,
    267,
    305,
    307,
    1014,
}


class L10nEsAeatMod303Report(models.Model):
    _inherit = "l10n.es.aeat.mod303.report"

    is_tax_agency_navarra = fields.Boolean(
        string="Navarra Company",
        compute="_compute_is_tax_agency_navarra",
        store=True,
        help="Indicates whether the company has the Navarra Regional Tax "
        "Agency configured as its tax agency.",
    )
    navarra_cifra_relativa = fields.Float(
        string="[55] Navarra relative figure (%)",
        digits=(11, 4),
        compute="_compute_navarra_cifra_relativa",
        store=True,
        readonly=False,
        help="Definitive relative figure percentage. In the first three "
        "quarters the definitive percentage from the previous year is used. "
        "In the fourth quarter the definitive percentage for the current year "
        "is reported.",
    )
    navarra_casilla_50 = fields.Float(
        string="[50] Navarra deductible VAT",
        compute="_compute_navarra_casilla_50",
        store=True,
        help="Total deductible VAT for the period. It corresponds to the sum "
        "of the deductible amounts of form 303 (boxes 29, 31, 33, 35, 37, 39, "
        "41, 42, 43 and 44), equivalent to box 50 of the F66.",
    )
    navarra_casilla_61 = fields.Float(
        string="[61] Navarra resulting amount",
        compute="_compute_navarra_casilla_61",
        store=True,
        help="Intermediate result of the general regime: (VAT accrued - VAT "
        "deductible) multiplied by the relative figure in box 55.",
    )
    navarra_casilla_62 = fields.Float(
        string="[62] Amount to offset from previous periods",
        compute="_compute_navarra_casilla_62",
        store=True,
        readonly=False,
        help="Negative balance pending offset from the previous return, only "
        "if it was chosen to offset it with Navarra.",
    )
    navarra_casilla_63 = fields.Float(
        string="[63] Navarra final result",
        compute="_compute_navarra_casilla_63",
        store=True,
        help="Box 61 - box 62 + annual regularization (box 69).",
    )
    navarra_casilla_69 = fields.Float(
        string="[69] Navarra annual regularization",
        related="regularizacion_anual",
        readonly=False,
        store=True,
        help="Annual regularization of the fourth quarter. It corresponds to "
        "box 68 of the 303 return.",
    )
    navarra_compensar = fields.Boolean(
        string="Leave the negative result to be offset",
        help="Check this box if the negative result of the period is left "
        "pending offset with the Navarra Regional Tax Agency instead of "
        "requesting a refund.",
    )
    navarra_modo_pago = fields.Selection(
        selection=[
            ("0", "No request for payment processing"),
            (
                "1",
                "If payable. Request to the Tax Agency to process payment "
                "with the bank in the name of the return electronically",
            ),
            (
                "2",
                "If payable. Request to the Tax Agency to process payment "
                "with the bank acting the presenter on behalf of the declarant "
                "electronically",
            ),
            (
                "3",
                "If payable. Request to the Tax Agency to process payment "
                "with the bank by provision of funds by the presenter of the "
                "return electronically",
            ),
            (
                "7",
                "If payable. Direct debit of the declarant",
            ),
        ],
        string="Navarra payment method",
        default="0",
        required=True,
    )
    navarra_casilla_164 = fields.Boolean(
        string="[164] Transactions over €3,005.06",
        help="Check this box if you have carried out transactions with any "
        "person or entity that, as a whole, have exceeded €3,005.06 during "
        "the calendar year.",
    )
    navarra_casilla_165 = fields.Boolean(
        string="[165] No transactions over €3,005.06",
        help="Check this box if you have not had any customer or supplier "
        "with whom you have exceeded €3,005.06 during the calendar year.",
    )
    navarra_casilla_264 = fields.Boolean(
        string="[264] Exempt transactions without right to deduction",
        help="Check this box if you have carried out exempt transactions "
        "without the right to deduction during the settlement period.",
    )
    navarra_casilla_265 = fields.Boolean(
        string="[265] No exempt transactions without right to deduction",
        help="Check this box if you have not carried out exempt transactions "
        "without the right to deduction during the settlement period.",
    )
    navarra_casilla_93 = fields.Boolean(
        string="[93] No activity",
        help="Check this box if no activity has been carried out during the "
        "settlement period.",
    )
    navarra_export_file = fields.Binary(
        string="Navarra export file",
        readonly=True,
        attachment=True,
    )
    navarra_export_filename = fields.Char(readonly=True)

    @api.depends("company_id.tax_agency_id")
    def _compute_is_tax_agency_navarra(self):
        navarra_agency = self.env.ref(
            "l10n_es_aeat.aeat_tax_agency_navarra", raise_if_not_found=False
        )
        for report in self:
            report.is_tax_agency_navarra = bool(
                navarra_agency and report.company_id.tax_agency_id == navarra_agency
            )

    def _get_navarra_previous_year_report(self):
        """Devuelve la última declaración del ejercicio anterior."""
        self.ensure_one()
        return self.search(
            [
                ("company_id", "=", self.company_id.id),
                ("year", "=", self.year - 1),
                ("period_type", "in", NAVARRA_LAST_PERIODS),
                ("state", "!=", "cancelled"),
            ],
            order="date_end desc, id desc",
            limit=1,
        )

    def _get_navarra_previous_report(self):
        """Devuelve la declaración inmediatamente anterior del mismo tipo."""
        self.ensure_one()
        return self.search(
            [
                ("company_id", "=", self.company_id.id),
                ("date_start", "<", self.date_start),
                ("state", "not in", ("draft", "cancelled")),
            ],
            order="date_end desc, id desc",
            limit=1,
        )

    @api.depends("company_id", "year", "period_type")
    def _compute_navarra_cifra_relativa(self):
        for report in self:
            if report.period_type in NAVARRA_LAST_PERIODS:
                if not report.navarra_cifra_relativa:
                    report.navarra_cifra_relativa = 100.0
                continue
            previous = report._get_navarra_previous_year_report()
            report.navarra_cifra_relativa = (
                previous.navarra_cifra_relativa if previous else 100.0
            )

    @api.depends("total_deducir")
    def _compute_navarra_casilla_50(self):
        for report in self:
            report.navarra_casilla_50 = report.total_deducir

    @api.depends(
        "total_devengado",
        "navarra_casilla_50",
        "navarra_cifra_relativa",
    )
    def _compute_navarra_casilla_61(self):
        for report in self:
            base = report.total_devengado - report.navarra_casilla_50
            report.navarra_casilla_61 = report.currency_id.round(
                base * report.navarra_cifra_relativa / 100.0
            )

    @api.depends("company_id", "date_start", "year", "period_type")
    def _compute_navarra_casilla_62(self):
        for report in self:
            previous = report._get_navarra_previous_report()
            amount = 0.0
            if (
                previous
                and previous.navarra_compensar
                and float_compare(
                    previous.navarra_casilla_63,
                    0.0,
                    precision_digits=report.currency_id.decimal_places,
                )
                < 0
            ):
                amount = -previous.navarra_casilla_63
            report.navarra_casilla_62 = report.currency_id.round(amount)

    @api.depends(
        "navarra_casilla_61",
        "navarra_casilla_62",
        "navarra_casilla_69",
    )
    def _compute_navarra_casilla_63(self):
        for report in self:
            report.navarra_casilla_63 = report.currency_id.round(
                report.navarra_casilla_61
                - report.navarra_casilla_62
                + report.navarra_casilla_69
            )

    def calculate(self):
        res = super().calculate()
        self._compute_navarra_cifra_relativa()
        self._compute_navarra_casilla_50()
        self._compute_navarra_casilla_61()
        self._compute_navarra_casilla_62()
        self._compute_navarra_casilla_63()
        return res

    @api.onchange("period_type", "return_last_period")
    def _onchange_navarra_resumen_anual(self):
        if self.period_type not in NAVARRA_LAST_PERIODS and not self.return_last_period:
            self.navarra_casilla_164 = False
            self.navarra_casilla_165 = False

    @api.constrains("navarra_cifra_relativa")
    def _check_navarra_cifra_relativa_range(self):
        for report in self.filtered("is_tax_agency_navarra"):
            if not 0.0 <= report.navarra_cifra_relativa <= 100.0:
                raise ValidationError(
                    _("The Navarra relative figure must be between 0 and 100.")
                )

    @api.constrains("navarra_cifra_relativa", "period_type", "year")
    def _check_navarra_cifra_relativa_anterior(self):
        for report in self.filtered("is_tax_agency_navarra"):
            if report.period_type in NAVARRA_LAST_PERIODS:
                continue
            previous = report._get_navarra_previous_year_report()
            if (
                previous
                and float_compare(
                    report.navarra_cifra_relativa,
                    previous.navarra_cifra_relativa,
                    precision_digits=4,
                )
                != 0
            ):
                raise ValidationError(
                    _(
                        "In the first three quarters the Navarra relative "
                        "figure must match the definitive percentage from the "
                        "previous year (%(pct)s %%)."
                    )
                    % {"pct": previous.navarra_cifra_relativa}
                )

    @api.constrains("navarra_modo_pago", "navarra_casilla_63")
    def _check_navarra_modo_pago(self):
        for report in self.filtered("is_tax_agency_navarra"):
            if (
                report.navarra_modo_pago != "0"
                and float_compare(
                    report.navarra_casilla_63,
                    0.0,
                    precision_digits=report.currency_id.decimal_places,
                )
                <= 0
            ):
                raise ValidationError(
                    _(
                        "The Navarra payment method can only be different from "
                        "0 when the final result (box 63) is positive."
                    )
                )

    @api.constrains(
        "navarra_casilla_164",
        "navarra_casilla_165",
        "period_type",
        "return_last_period",
        "state",
    )
    def _check_navarra_resumen_anual(self):
        for report in self.filtered("is_tax_agency_navarra"):
            if report.navarra_casilla_164 and report.navarra_casilla_165:
                raise ValidationError(
                    _(
                        "You cannot check boxes 164 and 165 of the Navarra "
                        "annual summary at the same time."
                    )
                )
            is_last_period = (
                report.period_type in NAVARRA_LAST_PERIODS or report.return_last_period
            )
            if not is_last_period and (
                report.navarra_casilla_164 or report.navarra_casilla_165
            ):
                raise ValidationError(
                    _(
                        "Boxes 164/165 are only filled in the fourth quarter "
                        "or in the cessation of activity period."
                    )
                )
            if (
                is_last_period
                and report.state in ("done", "posted")
                and not (report.navarra_casilla_164 or report.navarra_casilla_165)
            ):
                raise ValidationError(
                    _(
                        "You must check box 164 (YES) or 165 (NO) of the "
                        "Navarra annual summary."
                    )
                )

    @api.constrains(
        "navarra_casilla_264",
        "navarra_casilla_265",
        "state",
    )
    def _check_navarra_exentas(self):
        for report in self.filtered("is_tax_agency_navarra"):
            if report.navarra_casilla_264 and report.navarra_casilla_265:
                raise ValidationError(
                    _(
                        "You cannot check boxes 264 and 265 of Navarra exempt "
                        "transactions at the same time."
                    )
                )
            if report.state in ("done", "posted") and not (
                report.navarra_casilla_264 or report.navarra_casilla_265
            ):
                raise ValidationError(
                    _(
                        "You must check box 264 (YES) or 265 (NO) of Navarra "
                        "exempt transactions."
                    )
                )

    def _get_navarra_model_number(self):
        self.ensure_one()
        if self.period_type in NAVARRA_F69_PERIODS:
            return "F69"
        if self.period_type in NAVARRA_F66_PERIODS:
            return "F66"
        raise UserError(
            _("The period %(period)s cannot be exported to F66/F69.")
            % {"period": self.period_type}
        )

    def _get_navarra_period_code(self):
        self.ensure_one()
        if self.period_type in NAVARRA_F69_PERIODS:
            return f"{self.period_type[0]}00"
        month = int(self.period_type)
        quarter = (month - 1) // 3 + 1
        return f"{quarter}{month:02d}"

    def _get_navarra_nif(self):
        self.ensure_one()
        nif = re.sub(r"[^A-Z0-9]", "", (self.company_vat or "").upper())
        if nif.startswith("ES"):
            nif = nif[2:]
        if not nif:
            nif = re.sub(r"[^A-Z0-9]", "", (self.company_id.vat or "").upper())
            if nif.startswith("ES"):
                nif = nif[2:]
        if not nif:
            raise UserError(_("The company VAT number is required to export F66/F69."))
        return nif[:9].rjust(9, "0")

    @staticmethod
    def _navarra_ascii(value, size):
        text = unicodedata.normalize("NFKD", str(value or ""))
        text = "".join(char for char in text if not unicodedata.combining(char))
        text = re.sub(r"[^A-Za-z0-9 /.,&()\-]", " ", text)
        return text.upper()[:size].ljust(size)

    @staticmethod
    def _navarra_email_ascii(value, size):
        text = unicodedata.normalize("NFKD", str(value or ""))
        text = "".join(char for char in text if not unicodedata.combining(char))
        text = re.sub(r"[^A-Za-z0-9@._+\-]", "", text)
        return text[:size].ljust(size)

    def _get_navarra_phone(self):
        self.ensure_one()
        phone = re.sub(r"\D", "", self.contact_phone or "")
        return phone[-9:].rjust(9, "0")

    def _get_navarra_bank_account(self):
        self.ensure_one()
        account = ""
        if self.partner_bank_id and self.partner_bank_id.acc_number:
            account = re.sub(r"\D", "", self.partner_bank_id.acc_number)
        return account[-20:].rjust(20, "0")

    def _get_navarra_common_header(self):
        self.ensure_one()
        return (
            f"{self._get_navarra_model_number()}"
            f"{self.year:04d}"
            f"{self._get_navarra_period_code()}"
            "000000"
            f"{self._get_navarra_nif()}"
        )

    def _get_navarra_tax_amounts(self):
        self.ensure_one()
        amounts = {}
        for line in self.tax_line_ids:
            amounts[line.field_number] = (
                amounts.get(line.field_number, 0.0) + line.amount
            )
        return amounts

    def _get_navarra_annual_totals(self):
        self.ensure_one()
        if self.period_type not in NAVARRA_LAST_PERIODS:
            return 0.0, 0.0, 0.0
        reports = (
            self.search(
                [
                    ("company_id", "=", self.company_id.id),
                    ("year", "=", self.year),
                    ("date_end", "<=", self.date_end),
                    ("state", "not in", ("draft", "cancelled")),
                ]
            )
            | self
        )
        devengado = self.currency_id.round(sum(reports.mapped("total_devengado")))
        deducir = self.currency_id.round(sum(reports.mapped("total_deducir")))
        return devengado, deducir, self.currency_id.round(devengado - deducir)

    def _get_navarra_casilla_values(self):
        self.ensure_one()
        amounts = self._get_navarra_tax_amounts()

        def total(*field_numbers):
            return sum(amounts.get(number, 0.0) for number in field_numbers)

        values = {
            1: total(60),
            2: total(83),
            3: total(7, 150, 165),
            4: total(4, 153),
            5: total(1),
            6: total(22),
            7: total(16, 19),
            8: total(168),
            9: total(10),
            10: total(59),
            13: total(9, 152, 167),
            14: total(6, 155),
            15: total(3),
            16: total(24),
            17: total(18, 21),
            18: total(170),
            19: total(11),
            20: self.total_devengado,
            31: total(28),
            32: total(32, 34),
            39: total(36, 38),
            41: total(29),
            42: total(33, 35),
            43: total(42),
            45: total(43),
            49: total(37, 39),
            50: self.navarra_casilla_50,
            55: self.navarra_cifra_relativa,
            61: self.navarra_casilla_61,
            62: self.navarra_casilla_62,
            63: self.navarra_casilla_63,
            69: self.navarra_casilla_69,
            131: total(30),
            141: total(31),
            172: total(12),
            173: total(13),
            176: total(14),
            177: total(15),
            194: total(62),
            450: total(44),
        }
        if self.navarra_casilla_93:
            values[93] = 1.0
        if self.navarra_casilla_164:
            values[164] = 1.0
        if self.navarra_casilla_165:
            values[165] = 1.0
        if self.navarra_casilla_264:
            values[264] = 1.0
        if self.navarra_casilla_265:
            values[265] = 1.0
        if self.navarra_casilla_63 < 0:
            amount = self.currency_id.round(-self.navarra_casilla_63)
            if self.navarra_compensar:
                values[70] = amount
            else:
                values[64] = amount
        annual_devengado, annual_deducir, annual_result = (
            self._get_navarra_annual_totals()
        )
        if annual_devengado:
            values[110] = annual_devengado
        if annual_deducir:
            values[111] = annual_deducir
        if annual_result:
            values[112] = annual_result
        return values

    @staticmethod
    def _format_navarra_amount(amount, decimals):
        value = Decimal(str(amount or 0.0)).quantize(
            Decimal(1).scaleb(-decimals), rounding=ROUND_HALF_UP
        )
        scaled = int(abs(value) * (10**decimals))
        if scaled > 999999999999999:
            raise UserError(_("A Navarra box value exceeds the file size."))
        sign = "N" if value < 0 else " "
        return f"{sign}{str(scaled).zfill(15)}"

    @staticmethod
    def _get_navarra_decimals(code):
        if code == 55:
            return 4
        if code in NAVARRA_ZERO_DECIMAL_CASILLAS:
            return 0
        return 2

    def _get_navarra_casilla_items(self):
        self.ensure_one()
        values = self._get_navarra_casilla_values()
        codes = list(NAVARRA_CASILLA_ORDER)
        codes += sorted(set(values) - set(NAVARRA_CASILLA_ORDER))
        items = []
        for code in codes:
            if code not in values:
                continue
            amount = values[code]
            if code in NAVARRA_MARKER_CASILLAS:
                if not amount:
                    continue
                amount = 1.0
            elif code not in NAVARRA_ALWAYS_CASILLAS and abs(amount) < 0.005:
                continue
            decimals = self._get_navarra_decimals(code)
            items.append(f"{code:04d}{self._format_navarra_amount(amount, decimals)}")
        return items

    def _get_navarra_email(self):
        self.ensure_one()
        email = (self.contact_email or "").strip()
        if not email:
            return ""
        if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
            raise UserError(_("The contact email is not valid."))
        return self._navarra_email_ascii(email, 50)

    def _generate_navarra_file(self):
        self.ensure_one()
        model = self._get_navarra_model_number()
        common = self._get_navarra_common_header()
        name = self._navarra_ascii(self.company_id.name, 40)
        contact = self._navarra_ascii(self.contact_name, 40)
        phone = self._get_navarra_phone()
        items = self._get_navarra_casilla_items()
        chunks = [items[index : index + 10] for index in range(0, len(items), 10)]
        email = self._get_navarra_email()
        type3_count = 1 if email else 0
        counters = "".join(
            f"{count:08d}" for count in (1, len(chunks), type3_count, 0, 0, 0)
        )
        record0 = (
            f"0{model}{self.year:04d}{self._get_navarra_nif()}"
            f"{name}{' ' * 52}{counters}T{phone}{contact}{' ' * 30}{' ' * 13}"
        )
        previous_number = re.sub(r"\D", "", self.previous_number or "")
        statement = "S" if self.statement_type in ("C", "S") else " "
        record1 = (
            f"1{common}{name}{'0' * 14}T{phone}{contact}{'0' * 13} "
            f"{statement}{previous_number[-13:].rjust(13, '0')}"
            f"{self._get_navarra_bank_account()}"
            f"{self.navarra_modo_pago or '0'}{' ' * 22}{'0' * 8}{' ' * 28}{' ' * 13}"
        )
        records = [record0, record1]
        for chunk in chunks:
            slots = "".join(chunk)
            slots = slots.ljust(200)
            records.append(f"2{common}{slots}{' ' * 24}")
        if email:
            records.append(f"3{common}3003{email.ljust(50)}{' ' * 108}{' ' * 62}")
        for record in records:
            if len(record) != 250:
                raise UserError(_("The generated Navarra record has an invalid size."))
        return ("\r\n".join(records) + "\r\n").encode("latin-1")

    def button_navarra_export(self):
        self.ensure_one()
        data = self._generate_navarra_file()
        filename = (
            f"{self._get_navarra_model_number()}_"
            f"{self._get_navarra_nif()}_{self.year}_"
            f"{self._get_navarra_period_code()}.txt"
        )
        self.write(
            {
                "navarra_export_file": base64.b64encode(data),
                "navarra_export_filename": filename,
            }
        )
        return {
            "type": "ir.actions.act_url",
            "url": (
                f"/web/content/{self._name}/{self.id}/navarra_export_file/"
                f"{filename}?download=true"
            ),
            "target": "self",
        }
