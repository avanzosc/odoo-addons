# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models, api, _


class ResPartner(models.Model):
    _inherit = "res.partner"

    building_use_id = fields.Many2one(
        string=_("Building use"),
        comodel_name="building.use",
        copy=False,
    )
    building_section_ids = fields.One2many(
        string=_("Building Section/Area"),
        comodel_name="building.section",
        inverse_name="partner_id",
        copy=False,
    )
    service_start_date = fields.Date(
        string=_("Service Start Date"),
        copy=False,
    )
    service_end_date = fields.Date(
        string=_("Service End Date"),
        copy=False,
    )
    
    degree_title = fields.Char(
        string=_("Degree Title"),
        domain="[('is_company','=',False)]",
        help=_("Degree Title of the individual contact."),
    )
    membership_number = fields.Char(
        string=_("Membership Number"),
        domain="[('is_company','=',False)]",
        help=_("Membership number of the individual contact."),
    )
    emi = fields.Char(string=_("EMI"))
    epi = fields.Char(string=_("EPI"))
    
    # Maintainer
    maintainer_id = fields.Many2one(
        comodel_name="res.partner",
        string=_("Maintainer")
    )
    maintainer_emi = fields.Char(string=_("Maintainer EMI"), related="maintainer_id.emi")

    installer_id = fields.Many2one(
        comodel_name="res.partner",
        string=_("Installer")
    )
    installer_epi = fields.Char(string=_("Installer EPI"), related="installer_id.epi")
    certification_date = fields.Date(string=_("Date of Certificate from Installation Company"))
    administrator_id = fields.Many2one(
        comodel_name="res.partner",
        string=_("Administrator")
    )

    normativas_ids = fields.Many2many(
        "survey.question.normative",
        string=_("Normativas"),
        compute="_compute_normativas_ids",
    )
    
    # Project
    project_title = fields.Char(string=_("Project Title"))
    project_author_id = fields.Many2one(string=_("Project Author"), comodel_name="res.partner")
    project_author_degree = fields.Char(string=_("Project Author Degree"), related="project_author_id.degree_title")
    project_author_license = fields.Char(string=_("Project Author License"), related="project_author_id.membership_number")
    project_approved_date = fields.Date(string=_("Project Approved Date"))

    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(string=_("Director of Works Author"), comodel_name="res.partner")
    dof_author_degree = fields.Char(string=_("Director of Works Author Degree"), related="dof_author_id.degree_title")
    dof_author_license = fields.Char(string=_("Director of Works Author License"), related="dof_author_id.membership_number")
    dof_approved_date = fields.Date(string=_("Director of Works Approved Date"))


    @api.depends("service_start_date")
    def _compute_normativas_ids(self):
        for partner in self:
            partner.normativas_ids = self.env["survey.question.normative"].search(
                [
                    ("start_year", "<=", partner.service_start_date.year),
                    ("end_year", ">=", partner.service_start_date.year),
                ]
            )
