# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class EventEvent(models.Model):
    _inherit = "event.event"

    training_action_id = fields.Many2one(
        "event.training.action",
        string="Acción formativa",
        index=True,
        ondelete="restrict",
    )
    training_action_code = fields.Char(
        string="Código acción formativa",
        related="training_action_id.code",
        store=True,
        readonly=True,
    )
    training_funding_id = fields.Many2one(
        "event.training.funding",
        string="Expediente",
        related="training_action_id.funding_id",
        store=True,
        readonly=True,
    )
    training_funder_id = fields.Many2one(
        "res.partner",
        string="Financiador",
        related="training_action_id.funder_id",
        store=True,
        readonly=True,
    )
    training_payer_id = fields.Many2one(
        "res.partner",
        string="Empresa pagadora",
        related="training_action_id.payer_id",
        store=True,
        readonly=True,
    )
    training_specialty_code = fields.Char(
        string="Código especialidad SEPE",
        related="training_action_id.specialty_code",
        store=True,
        readonly=True,
    )
    training_modality = fields.Selection(
        related="training_action_id.modality",
        string="Modalidad formación",
        store=True,
        readonly=True,
    )
    training_hours = fields.Float(
        string="Horas previstas formación",
        related="training_action_id.total_hours",
        store=True,
        readonly=True,
    )
