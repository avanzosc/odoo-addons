# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        comodel_name="building.use",
        string="Building use",
    )
    building_section_ids = fields.One2many(
        comodel_name="building.section",
        inverse_name="partner_id",
        string="Building Section/Area",
    )
    service_start_date = fields.Date()
    service_end_date = fields.Date()
    alternative_text = fields.Char(
        copy=False,
    )
    number_of_floors = fields.Char()
    risk = fields.Char(
        copy=False,
    )
    area = fields.Float(
        string="Surface",
        default=0.0,
        copy=False,
    )
    evacuation_height = fields.Float()
    configuration = fields.Selection(
        selection=[
            ("A", "A"),
            ("B", "B"),
            ("C", "C"),
            ("D", "D"),
            ("E", "E"),
        ],
    )
    file_number = fields.Char()
    installation_number = fields.Char()
    certification_text = fields.Text()
    degree_title = fields.Char(
        domain="[('is_company','=',False)]",
        help="Degree Title of the individual contact.",
    )
    membership_number = fields.Char(
        domain="[('is_company','=',False)]",
        help="Membership number of the individual contact.",
    )
    emi = fields.Char(
        string="EMI",
    )
    epi = fields.Char(
        string="EPI",
    )
    # Maintainer
    maintainer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Maintainer",
    )
    maintainer_emi = fields.Char(
        string="Maintainer EMI",
        related="maintainer_id.emi",
    )
    installer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Installer",
    )
    installer_epi = fields.Char(
        string="Installer EPI",
        related="installer_id.epi",
    )
    certification_date = fields.Date(
        string="Date of Certificate from Installation Company",
    )
    administrator_id = fields.Many2one(
        comodel_name="res.partner",
        string="Administrator",
    )
    normativas_ids = fields.Many2many(
        comodel_name="survey.question.normative",
        string="Normativas",
        compute="_compute_normativas_ids",
    )
    dof_author_degree = fields.Char(
        string="Director of Works Author Degree",
        related="inspected_building_id.dof_author_degree",
    )
    # Project
    project_title = fields.Char()
    project_author_id = fields.Many2one(
        comodel_name="res.partner",
        string="Project Author",
    )
    project_author_degree = fields.Char(
        related="project_author_id.degree_title",
    )
    project_author_license = fields.Char(
        related="project_author_id.membership_number",
    )
    project_approved_date = fields.Date()
    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(
        comodel_name="res.partner",
        string="Director of Works Author",
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
