# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTrainingFunding(models.Model):
    _name = "event.training.funding"
    _description = "Expediente de financiación de formación"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "year desc, code, id desc"

    code = fields.Char(
        string="Código expediente", required=True, index=True, tracking=True, copy=False
    )
    name = fields.Char(string="Nombre expediente", required=True, tracking=True)
    contract_type = fields.Selection(
        [
            ("grant", "Subvención"),
            ("tender", "Licitación"),
            ("agreement", "Convenio"),
            ("contract", "Contrato"),
        ],
        string="Tipo expediente",
        required=True,
        default="grant",
        tracking=True,
    )
    year = fields.Integer(
        string="Ejercicio",
        required=True,
        default=lambda self: fields.Date.context_today(self).year,
    )
    official_reference = fields.Char(string="Nº expediente oficial")
    funder_id = fields.Many2one("res.partner", string="Financiador", tracking=True)
    customer_id = fields.Many2one("res.partner", string="Empresa contratante")
    payer_id = fields.Many2one("res.partner", string="Empresa pagadora")
    beneficiary_id = fields.Many2one("res.partner", string="Entidad beneficiaria")
    amount_awarded = fields.Monetary(
        string="Importe concedido", currency_field="currency_id"
    )
    currency_id = fields.Many2one(
        "res.currency",
        string="Moneda",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    award_date = fields.Date(string="Fecha adjudicación")
    date_start = fields.Date(string="Fecha inicio")
    date_end = fields.Date(string="Fecha fin")
    justification_deadline = fields.Date(string="Fecha límite justificación")
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("submitted", "Presentado"),
            ("awarded", "Adjudicado"),
            ("running", "En ejecución"),
            ("justified", "Justificado"),
            ("closed", "Cerrado"),
        ],
        string="Estado",
        default="draft",
        required=True,
        tracking=True,
    )
    description = fields.Html(string="Descripción")
    action_ids = fields.One2many(
        "event.training.action", "funding_id", string="Acciones formativas"
    )
    action_count = fields.Integer(string="Nº acciones", compute="_compute_action_count")

    _sql_constraints = [
        ("code_uniq", "unique(code)", "El código del expediente debe ser único."),
    ]

    @api.depends("action_ids")
    def _compute_action_count(self):
        for record in self:
            record.action_count = len(record.action_ids)

    @api.constrains("date_start", "date_end")
    def _check_dates(self):
        for record in self:
            if (
                record.date_start
                and record.date_end
                and record.date_end < record.date_start
            ):
                raise ValidationError(
                    _("La fecha fin no puede ser anterior a la fecha inicio.")
                )
