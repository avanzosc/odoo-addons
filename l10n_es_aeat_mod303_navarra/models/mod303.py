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
        string="Compañía Navarra",
        compute="_compute_is_tax_agency_navarra",
        store=True,
        help="Indica si la compañía tiene configurada la Hacienda Foral de "
        "Navarra como agencia tributaria.",
    )
    navarra_cifra_relativa = fields.Float(
        string="[55] Cifra relativa Navarra (%)",
        digits=(11, 4),
        compute="_compute_navarra_cifra_relativa",
        store=True,
        readonly=False,
        help="Porcentaje definitivo de cifra relativa. En los tres primeros "
        "trimestres se toma el porcentaje definitivo del año anterior. En el "
        "cuarto trimestre se informa el porcentaje definitivo del propio año.",
    )
    navarra_casilla_50 = fields.Float(
        string="[50] IVA deducible Navarra",
        compute="_compute_navarra_casilla_50",
        store=True,
        help="Total del IVA deducible del periodo. Se corresponde con la suma "
        "de las cuotas deducibles del 303 (casillas 29, 31, 33, 35, 37, 39, "
        "41, 42, 43 y 44), equivalente a la casilla 50 del F66.",
    )
    navarra_casilla_61 = fields.Float(
        string="[61] Cuota resultante Navarra",
        compute="_compute_navarra_casilla_61",
        store=True,
        help="Resultado intermedio del régimen general: (IVA devengado - IVA "
        "deducible) multiplicado por la cifra relativa de la casilla 55.",
    )
    navarra_casilla_62 = fields.Float(
        string="[62] Cuota a compensar de periodos anteriores",
        compute="_compute_navarra_casilla_62",
        store=True,
        readonly=False,
        help="Saldo negativo pendiente de compensar de la declaración "
        "anterior, únicamente si se optó por compensarlo con Navarra.",
    )
    navarra_casilla_63 = fields.Float(
        string="[63] Resultado final Navarra",
        compute="_compute_navarra_casilla_63",
        store=True,
        help="Casilla 61 - casilla 62 + regularización anual (casilla 69).",
    )
    navarra_casilla_69 = fields.Float(
        string="[69] Regularización anual Navarra",
        related="regularizacion_anual",
        readonly=False,
        store=True,
        help="Regularización anual del cuarto trimestre. Se corresponde con "
        "la casilla 68 del modelo 303.",
    )
    navarra_compensar = fields.Boolean(
        string="Dejar el resultado negativo para compensar",
        help="Marque esta casilla si el resultado negativo del periodo se "
        "deja pendiente de compensar con la Hacienda Foral de Navarra en "
        "lugar de solicitar la devolución.",
    )
    navarra_modo_pago = fields.Selection(
        selection=[
            ("0", "No petición de la tramitación del pago"),
            (
                "1",
                "Si sale a pagar. Petición a Hacienda de que tramite con el "
                "banco el pago en nombre propio de la declaración "
                "telemáticamente",
            ),
            (
                "2",
                "Si sale a pagar. Petición a Hacienda de que tramite con el "
                "banco el pago actuando el presentador en representación del "
                "declarante telemáticamente",
            ),
            (
                "3",
                "Si sale a pagar. Petición a Hacienda de que tramite con el "
                "banco el pago por provisión de fondos por parte del "
                "presentador de la declaración telemáticamente",
            ),
            (
                "7",
                "Si sale a pagar. Domiciliación bancaria del declarante",
            ),
        ],
        string="Modo de pago Navarra",
        default="0",
        required=True,
    )
    navarra_casilla_164 = fields.Boolean(
        string="[164] Operaciones de más de 3.005,06 €",
        help="Marque esta casilla si ha efectuado operaciones con alguna "
        "persona o entidad que, en su conjunto global, hayan superado "
        "3.005,06 € durante el año natural.",
    )
    navarra_casilla_165 = fields.Boolean(
        string="[165] Sin operaciones de más de 3.005,06 €",
        help="Marque esta casilla si no ha tenido ningún cliente o proveedor "
        "con el que haya superado 3.005,06 € durante el año natural.",
    )
    navarra_casilla_264 = fields.Boolean(
        string="[264] Operaciones exentas sin derecho a deducción",
        help="Marque esta casilla si ha realizado operaciones exentas sin "
        "derecho a la deducción durante el periodo de liquidación.",
    )
    navarra_casilla_265 = fields.Boolean(
        string="[265] Sin operaciones exentas sin derecho a deducción",
        help="Marque esta casilla si no ha realizado operaciones exentas sin "
        "derecho a la deducción durante el periodo de liquidación.",
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
                    _("La cifra relativa de Navarra debe estar entre 0 y " "100.")
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
                        "En los tres primeros trimestres la cifra relativa de "
                        "Navarra debe coincidir con el porcentaje definitivo "
                        "del año anterior (%(pct)s %%)."
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
                        "El modo de pago de Navarra solo puede ser distinto "
                        "de 0 cuando el resultado final (casilla 63) es "
                        "positivo."
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
                        "No puede marcar simultáneamente las casillas 164 y "
                        "165 del resumen anual de Navarra."
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
                        "Las casillas 164/165 solo se rellenan en el cuarto "
                        "trimestre o en el periodo de cese de la actividad."
                    )
                )
            if (
                is_last_period
                and report.state in ("done", "posted")
                and not (report.navarra_casilla_164 or report.navarra_casilla_165)
            ):
                raise ValidationError(
                    _(
                        "Debe marcar la casilla 164 (SÍ) o la 165 (NO) del "
                        "resumen anual de Navarra."
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
                        "No puede marcar simultáneamente las casillas 264 y "
                        "265 de operaciones exentas de Navarra."
                    )
                )
            if report.state in ("done", "posted") and not (
                report.navarra_casilla_264 or report.navarra_casilla_265
            ):
                raise ValidationError(
                    _(
                        "Debe marcar la casilla 264 (SÍ) o la 265 (NO) de "
                        "operaciones exentas de Navarra."
                    )
                )
