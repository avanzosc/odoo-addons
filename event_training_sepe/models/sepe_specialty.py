# Copyright 2026 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class SepeTrainingSpecialty(models.Model):
    _name = "sepe.training.specialty"
    _description = "Especialidad formativa SEPE"
    _rec_name = "name"
    _order = "code, version, id"

    code = fields.Char(string="Código", required=True, index=True)
    name = fields.Char(string="Denominación", required=True, index=True)
    version = fields.Char(
        string="Versión",
        help="Texto para conservar versiones tal como aparecen en el catálogo.",
    )
    professional_family = fields.Char(string="Familia profesional", index=True)
    professional_area = fields.Char(string="Área profesional", index=True)
    transversal_competence = fields.Char(string="Competencia transversal")
    qualification_level = fields.Char(string="Nivel de cualificación")
    delivery_modality = fields.Char(string="Modalidad de impartición")
    total_duration = fields.Float(string="Duración total", digits=(16, 2))
    in_person_duration = fields.Float(
        string="Duración total de la parte presencial (teleformación o mixta)",
        digits=(16, 2),
    )
    related_occupations = fields.Text(string="Ocupaciones relacionadas")
