# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        string="Building use",
        comodel_name="building.use",
        copy=False,
    )
    building_section_ids = fields.One2many(
        string="Building Section/Area",
        comodel_name="building.section",
        inverse_name="partner_id",
        copy=False,
    )
    service_start_date = fields.Date(
        copy=False,
    )
    service_end_date = fields.Date(
        copy=False,
    )
    degree_title = fields.Char(
        help="Degree Title of the individual contact.",
    )
    membership_number = fields.Char(
        help="Membership number of the individual contact.",
    )
    emi = fields.Char(string="EMI")
    epi = fields.Char(string="EPI")

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
        "survey.question.normative",
        string="Normativas",
        compute="_compute_normativas_ids",
    )
    # Project
    project_title = fields.Char()
    project_author_id = fields.Many2one(
        string="Project Author",
        comodel_name="res.partner",
    )
    project_author_degree = fields.Char(
        string="Project Author Degree",
        related="project_author_id.degree_title",
    )
    project_author_license = fields.Char(
        string="Project Author License",
        related="project_author_id.membership_number",
    )
    project_approved_date = fields.Date()
    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(
        string="Director of Works Author",
        comodel_name="res.partner",
    )
    dof_author_degree = fields.Char(
        string="Director of Works Author Degree",
        related="dof_author_id.degree_title",
    )
    dof_author_license = fields.Char(
        string="Director of Works Author License",
        related="dof_author_id.membership_number",
    )
    dof_approved_date = fields.Date(string="Director of Works Approved Date")

    @api.depends("service_start_date")
    def _compute_normativas_ids(self):
        normative_obj = self.env["survey.question.normative"]
        for partner in self:
            partner.normativas_ids = normative_obj.search(
                [
                    ("start_year", "<=", partner.service_start_date.year),
                    ("end_year", ">=", partner.service_start_date.year),
                ]
            )
