# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class BuildingSection(models.Model):
    _name = "building.section"
    _description = "Building Section/Area"

    name = fields.Char(string=_("Description"), required=True, copy=False)
    risk = fields.Char(string=_("Risk"), copy=False)
    section_use = fields.Many2one("building.use", string=_("Section Use"))

    superficie = fields.Float(string=_("Surface"), default=0.0, copy=False)
    partner_id = fields.Many2one(
        string=_("Contact"), comodel_name="res.partner", required=True, copy=False
    )
    evacuation_height = fields.Float(string=_('Evacuation Height'))

    # Project
    project_title = fields.Char(string=_("Project Title"))
    project_author_id = fields.Many2one(string=_("Project Author"), comodel_name="res.partner")
    project_author_degree = fields.Char(string=_("Project Author Degree"), related="project_author_id.degree_title")
    project_author_license = fields.Char(string=_("Project Author License"), related="project_author_id.colegiado_numero")
    project_approved_date = fields.Date(string=_("Project Approved Date"))

    # Certificate of Final Work Direction
    dof_author_id = fields.Many2one(string=_("Director of Works Author"), comodel_name="res.partner")
    dof_author_degree = fields.Char(string=_("Director of Works Author Degree"), related="dof_author_id.membership_number")
    dof_author_license = fields.Char(string=_("Director of Works Author License"), related="dof_author_id.colegiado_numero")
    dof_approved_date = fields.Date(string=_("Director of Works Approved Date"))

