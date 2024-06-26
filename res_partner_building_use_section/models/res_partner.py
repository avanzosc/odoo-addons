# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        "building.use",
        "Building use",
    )
    building_section_ids = fields.One2many(
        "building.section",
        "partner_id",
        "Building Section/Area",
    )
    service_start_date = fields.Date(
        "Service Start Date",
    )
    service_end_date = fields.Date(
        "Service End Date",
    )
    alternative_text = fields.Char(
        "Alternative Text",
        copy=False,
    )
    number_of_floors = fields.Char(
        "Number of Plants",
    )
    risk = fields.Char(
        "Risk",
        copy=False,
    )
    area = fields.Float(
        "Surface",
        default=0.0,
        copy=False,
    )
    evacuation_height = fields.Float(
        "Evacuation Height",
    )
    configuration = fields.Selection(
        [
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
        ],
        "Configuration",
    )
    file_number = fields.Char(
        "File Number",
    )
    installation_number = fields.Char(
        "Installation Number",
    )
    certification_text = fields.Text(
        "Certification Text",
    )
    degree_title = fields.Char(
        "Degree Title",
        domain="[('is_company','=',False)]",
        help="Degree Title of the individual contact.",
    )
    membership_number = fields.Char(
        "Membership Number",
        domain="[('is_company','=',False)]",
        help="Membership number of the individual contact.",
    )
    emi = fields.Char(
        "EMI",
    )
    epi = fields.Char(
        "EPI",
    )
    # Maintainer
    maintainer_id = fields.Many2one(
        "res.partner",
        "Maintainer",
    )
    maintainer_emi = fields.Char(
        "Maintainer EMI",
        related="maintainer_id.emi",
    )
    installer_id = fields.Many2one(
        "res.partner",
        "Installer",
    )
    installer_epi = fields.Char(
        "Installer EPI",
        related="installer_id.epi",
    )
    certification_date = fields.Date(
        "Date of Certificate from Installation Company",
    )
    administrator_id = fields.Many2one(
        "res.partner",
        "Administrator",
    )
    normativas_ids = fields.Many2many(
        "survey.question.normative",
        "Normativas",
        compute="_compute_normativas_ids",
    )
    dof_author_degree = fields.Char(
        "Director of Works Author Degree",
        related="inspected_building_id.dof_author_degree",
    )
    # Project
    project_title = fields.Char(
        "Project Title",
    )
    project_author_id = fields.Many2one(
        "res.partner",
        "Project Author",
    )
    project_author_degree = fields.Char(
        "Project Author Degree",
        related="project_author_id.degree_title",
    )
    project_author_license = fields.Char(
        "Project Author License",
        related="project_author_id.membership_number",
    )
    project_approved_date = fields.Date(
        "Project Approved Date",
    )
    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(
        "res.partner",
        "Director of Works Author",
    )
    dof_author_degree = fields.Char(
        "Director of Works Author Degree",
        related="dof_author_id.degree_title",
    )
    dof_author_license = fields.Char(
        "Director of Works Author License",
        related="dof_author_id.membership_number",
    )
    dof_approved_date = fields.Date(
        "Director of Works Approved Date",
    )
