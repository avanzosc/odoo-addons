# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
import logging

from odoo import api, fields, models
from odoo.http import request

_logger = logging.getLogger(__name__)

class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    inspected_building_id = fields.Many2one(
        "res.partner",
        string="Inspected Building",
    )
    maintainer_id = fields.Many2one(
        "res.partner",
        string="Maintainer",
        related="inspected_building_id.maintainer_id",
    )
    maintainer_emi = fields.Char(
        string="Maintainer EMI",
        related="maintainer_id.emi",
    )
    installer_id = fields.Many2one(
        "res.partner",
        string="Installer",
        related="inspected_building_id.installer_id",
    )
    installer_epi = fields.Char(
        string="Installer EPI",
        related="installer_id.epi",
    )
    administrator_id = fields.Many2one(
        "res.partner",
        string="Administrator",
        related="inspected_building_id.administrator_id",
    )
    configuration = fields.Selection(
        string="Configuration",
        related="building_section_id.configuration",
        store=True,
    )
    building_section_id = fields.Many2one(
        "building.section",
        string="Building Section/Area",
    )
    section_ids = fields.One2many(
        "building.section",
        "partner_id",
        string="Inspected Building Section/Area",
        related="inspected_building_id.building_section_ids",
    )
    building_use_id = fields.Many2one(
        "building.use",
        string="Building type",
        related="inspected_building_id.building_use_id",
        store=True,
    )
    is_industrial = fields.Boolean(
        string="Industrial",
        related="building_use_id.is_industrial",
        store=True,
    )
    risk = fields.Char(
        string="Risk",
        related="building_section_id.risk",
        store=True,
    )
    area = fields.Float(
        string="Superficie",
        related="building_section_id.area",
        store=True,
    )
    file_number = fields.Char(
        string="File Number",
        related="inspected_building_id.file_number",
        store=True,
    )
    number_of_floors = fields.Char(
        string="Number of Plants",
        related="inspected_building_id.number_of_floors",
        store=True,
    )
    installation_number = fields.Char(
        string="Installation Number",
        related="inspected_building_id.installation_number",
    )
    act_number = fields.Char(
        string="Act Number",
    )
    inspection_start_date = fields.Datetime(
        string="Inspection Start Date",
    )
    inspection_end_date = fields.Datetime(
        string="Inspection End Date",
    )
    inspector_id = fields.Many2one(
        "res.partner",
        string="Inspector",
    )
    inspection_type = fields.Selection(
        [
            ("periodic", "Periodic"),
            ("volunteer", "Volunteer"),
            ("correction_of_deficiencies", "Correction of Deficiencies"),
        ],
        string="Inspection Type",
    )
    date_deficiency_correction = fields.Date(
        string="Date Deficiency Correction",
    )
    next_inspection_date = fields.Date(
        string="Next Inspection Date",
    )
    installed_equipment_ids = fields.Many2many(
        "installed.equipment",
        string="Installed Equipment",
    )

    # Project
    project_title = fields.Char(
        string="Project Title",
        related="inspected_building_id.project_title",
    )
    project_author_id = fields.Many2one(
        "res.partner",
        string="Project Author",
        related="inspected_building_id.project_author_id",
    )
    project_author_degree = fields.Char(
        string="Project Author Degree",
        related="inspected_building_id.project_author_id.degree_title",
    )
    project_author_license = fields.Char(
        string="Project Author License",
        related="inspected_building_id.project_author_id.membership_number",
    )
    project_approved_date = fields.Date(
        string="Project Approved Date",
        related="inspected_building_id.project_approved_date",
    )

    certification_date = fields.Date(
        string="Certification Date",
        related="inspected_building_id.certification_date",
    )

    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(
        "res.partner",
        string="Director of Works Author",
        related="inspected_building_id.dof_author_id",
    )
    dof_author_degree = fields.Char(
        string="Director of Works Author Degree",
        related="inspected_building_id.dof_author_id.degree_title",
    )
    dof_author_license = fields.Char(
        string="Director of Works Author License",
        related="inspected_building_id.dof_author_id.membership_number",
    )
    dof_approved_date = fields.Date(
        string="Director of Works Approved Date",
        related="inspected_building_id.dof_approved_date",
    )

    survey_report_fussion = fields.Many2many(
        "survey.user_input",
        string="Survey Report Fussion",
        relation="survey_report_fussion_rel",
        column1="survey_report_fussion_id",
        column2="survey_report_id",
    )
    remove_title_from_report = fields.Boolean(
        string="Remove Title From Report",
    )
    remove_upper_text_from_report = fields.Boolean(
        string="Remove Upper Text From Report",
    )

    @api.model_create_multi
    def create(self, vals_list):
        inputs = super().create(vals_list)
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
