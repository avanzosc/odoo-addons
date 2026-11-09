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
* [164]/[165] Resumen anual de operaciones.
* [264]/[265] Operaciones exentas sin derecho a deducción.
"""

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare

NAVARRA_LAST_PERIODS = ("4T", "12")


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
