# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class EventTrainingAction(models.Model):
    _name = "event.training.action"
    _description = "Acción formativa SEPE"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _rec_name = "name"
    _order = "funding_id, code, id"

    code = fields.Char(string="Código acción", required=True, index=True, tracking=True)
    name = fields.Char(string="Nombre acción", required=True, tracking=True)
    funding_id = fields.Many2one(
        "event.training.funding",
        string="Expediente / Licitación",
        required=True,
        index=True,
        ondelete="restrict",
        tracking=True,
    )
    funder_id = fields.Many2one(
        "res.partner",
        string="Financiador",
        related="funding_id.funder_id",
        store=True,
        readonly=True,
    )
    customer_id = fields.Many2one(
        "res.partner",
        string="Empresa contratante",
        related="funding_id.customer_id",
        store=True,
        readonly=True,
    )
    payer_id = fields.Many2one(
        "res.partner",
        string="Empresa pagadora",
        related="funding_id.payer_id",
        store=True,
        readonly=True,
    )
    year = fields.Integer(
        string="Ejercicio", related="funding_id.year", store=True, readonly=True
    )
    specialty_id = fields.Many2one(
        comodel_name="sepe.training.specialty",
        string="Especialidad SEPE",
        index=True,
        ondelete="restrict",
    )
    specialty_code = fields.Char(
        string="Código especialidad SEPE",
        related="specialty_id.code",
        store=True,
        readonly=True,
    )
    professional_family = fields.Char(string="Familia profesional")
    professional_area = fields.Char(string="Área profesional")
    modality = fields.Selection(
        [
            ("classroom", "Presencial"),
            ("online", "Teleformación"),
            ("mixed", "Mixta"),
        ],
        string="Modalidad",
        required=True,
        default="classroom",
    )
    total_hours = fields.Float(string="Horas totales", required=True)
    classroom_hours = fields.Float(string="Horas presenciales")
    online_hours = fields.Float(string="Horas teleformación")
    objectives = fields.Html(string="Objetivos")
    contents = fields.Html(string="Contenidos")
    entry_requirements = fields.Html(string="Requisitos de acceso")
    target_audience = fields.Html(string="Colectivo destinatario")
    planned_attendees = fields.Integer(string="Alumnos previstos por grupo")
    planned_groups = fields.Integer(string="Grupos previstos")
    allocated_amount = fields.Monetary(
        string="Importe asignado", currency_field="currency_id"
    )
    currency_id = fields.Many2one(
        "res.currency", related="funding_id.currency_id", store=True, readonly=True
    )
    execution_deadline = fields.Date(
        string="Fecha límite ejecución",
        related="funding_id.date_end",
        store=True,
        readonly=True,
    )
    state = fields.Selection(
        [
            ("draft", "Borrador"),
            ("approved", "Aprobada"),
            ("running", "En ejecución"),
            ("finished", "Finalizada"),
            ("closed", "Cerrada"),
        ],
        string="Estado",
        required=True,
        default="draft",
        tracking=True,
    )
    description = fields.Html(string="Descripción")
    event_ids = fields.One2many(
        "event.event", "training_action_id", string="Eventos / Cursos"
    )
    event_count = fields.Integer(string="Nº eventos", compute="_compute_event_count")
    grant_program_id = fields.Many2one(
        "grant.program",
        string="Línea subvencional",
        ondelete="restrict",
        index=True,
    )

    _sql_constraints = [
        (
            "funding_code_uniq",
            "unique(funding_id, code)",
            "El código de acción debe ser único dentro del expediente.",
        ),
    ]

    @api.depends("event_ids")
    def _compute_event_count(self):
        for record in self:
            record.event_count = len(record.event_ids)

    @api.constrains(
        "total_hours",
        "classroom_hours",
        "online_hours",
        "planned_attendees",
        "planned_groups",
    )
    def _check_quantities(self):
        for record in self:
            if (
                min(
                    record.total_hours,
                    record.classroom_hours,
                    record.online_hours,
                    record.planned_attendees,
                    record.planned_groups,
                )
                < 0
            ):
                raise ValidationError(
                    _("Las horas y cantidades previstas no pueden ser negativas.")
                )
