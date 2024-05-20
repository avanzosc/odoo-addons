# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.http import request

import logging

_logger = logging.getLogger(__name__)


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    inspected_building_id = fields.Many2one(
        string=_("Inspected Building"),
        comodel_name="res.partner",
        copy=False,
    )
    maintainer_id = fields.Many2one(
        related="inspected_building_id.maintainer_id",
        string=_("Maintainer"),
        comodel_name="res.partner",
    )
    installer_id = fields.Many2one(
        related="inspected_building_id.installer_id",
        string=_("Installer"),
        comodel_name="res.partner",
    )
    administrator_id = fields.Many2one(
        related="inspected_building_id.administrator_id",
        string=_("Administrator"),
        comodel_name="res.partner",
    )

    building_section_id = fields.Many2one(
        string=_("Building Section/Area"),
        comodel_name="building.section",
        copy=False,
    )
    section_ids = fields.One2many(
        string=_("Inspected Building Section/Area"),
        comodel_name="building.section",
        copy=False,
        related="inspected_building_id.building_section_ids",
    )
    building_use_id = fields.Many2one(
        string=_("Building type"),
        comodel_name="building.use",
        related="inspected_building_id.building_use_id",
        store=True,
        copy=False,
    )
    risk = fields.Char(
        string=_("Risk"), related="building_section_id.risk", store=True, copy=False
    )
    superficie = fields.Float(
        string=_("Superficie"),
        related="building_section_id.superficie",
        store=True,
        copy=False,
    )
    file_number = fields.Char(
        string=_("File Number"),
        related="inspected_building_id.file_number",
        store=True,
        copy=False,
    )
    act_number = fields.Char(
        string=_("Act Number"),
        copy=False,
    )
    inspection_start_date = fields.Datetime(
        string=_("Inspection Start Date"),
        copy=False,
    )
    inspection_end_date = fields.Datetime(
        string=_("Inspection End Date"),
        copy=False,
    )
    inspector_id = fields.Many2one(
        string=_("Inspector"),
        comodel_name="res.partner",
        copy=False,
    )
    inspection_type = fields.Selection(
        selection=[("periodic", _("Periodic")), ("volunteer", _("Volunteer"))],
        string=_("Inspection Type"),
        copy=False,
    )

    # Project
    project_title = fields.Char(
        string=_("Project Title"), related="inspected_building_id.project_title"
    )
    project_author_id = fields.Many2one(
        string=_("Project Author"),
        comodel_name="res.partner",
        related="inspected_building_id.project_author_id",
    )
    project_author_degree = fields.Char(
        string=_("Project Author Degree"),
        related="inspected_building_id.project_author_id.degree_title",
    )
    project_author_license = fields.Char(
        string=_("Project Author License"),
        related="inspected_building_id.project_author_id.membership_number",
    )
    project_approved_date = fields.Date(
        string=_("Project Approved Date"),
        related="inspected_building_id.project_approved_date",
    )

    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(
        string=_("Director of Works Author"),
        comodel_name="res.partner",
        related="inspected_building_id.dof_author_id",
    )
    dof_author_degree = fields.Char(
        string=_("Director of Works Author Degree"),
        related="inspected_building_id.dof_author_id.degree_title",
    )
    dof_author_license = fields.Char(
        string=_("Director of Works Author License"),
        related="inspected_building_id.dof_author_id.membership_number",
    )
    dof_approved_date = fields.Date(
        string=_("Director of Works Approved Date"),
        related="inspected_building_id.dof_approved_date",
    )

    @api.model_create_multi
    def create(self, vals_list):
        inputs = super(SurveyUserInput, self).create(vals_list)
        for input in inputs:
            if "building" in self.env.context:
                input.inspected_building_id = self.env.context.get("building").id
        return inputs

    def action_start_survey(self):
        current_user_partner = self.env.user.partner_id

        if current_user_partner:
            # Asignar el ID del socio asociado con el usuario actual al partner_id del survey_user_input
            self.partner_id = current_user_partner.id
        else:
            # Usuario administrador es id = 3
            self.partner_id = 3

        # Obtener la URL completa de la solicitud actual
        full_url = request.httprequest.url

        # Encontrar el índice del primer punto y el primer slash después de ese punto
        dot_index = full_url.find(".")
        slash_index = full_url.find("/", dot_index)

        base_url = False

        # Extraer la URL base
        if dot_index != -1 and slash_index != -1:
            base_url = full_url[:slash_index]

        if not base_url:
            base_url = self.env["ir.config_parameter"].get_param("web.base.url")

        survey_id = self.survey_id
        access_token = survey_id.access_token
        answer_token = self.access_token
        url = "{}/survey/start/{}?answer_token={}".format(
            base_url, access_token, answer_token
        )
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }
