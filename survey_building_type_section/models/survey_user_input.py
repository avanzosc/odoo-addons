# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models


class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    inspected_building_id = fields.Many2one(
        string="Inspected Building", comodel_name="res.partner", copy=False,
    )
    building_section_id = fields.Many2one(
        string="Building Section/Area", comodel_name="building.section",
        copy=False,
    )
    section_ids = fields.One2many(
        string="Inspected Building Section/Area",
        comodel_name="building.section", copy=False,
        related="inspected_building_id.building_section_ids"
    )
    building_type_id = fields.Many2one(
        string="Building type", comodel_name="building.type",
        related="inspected_building_id.building_type_id", store=True,
        copy=False,
    )
    risk_use = fields.Char(
        string="Risk/User", related="building_section_id.risk_use",
        store=True, copy=False
    )
    superficie = fields.Float(
        string="Superficie", related="building_section_id.superficie",
        store=True, copy=False
    )
    file_number = fields.Char(
        string="File Number", related="inspected_building_id.file_number",
        store=True, copy=False,
    )
    act_number = fields.Char(
        string="Act Number", copy=False,
    )
    inspection_start_date = fields.Datetime(
        string="Inspection Start Date", copy=False,
    )
    inspection_end_date = fields.Datetime(
        string="Inspection End Date", copy=False,
    )
    inspector_id = fields.Many2one(
        string="Inspector", comodel_name="res.partner", copy=False,
    )
    inspection_type = fields.Selection(
        selection=[
            ("periodic", _("Periodic")),
            ("volunteer", _("Volunteer"))],
        string="Inspection Type", copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        inputs = super(SurveyUserInput, self).create(vals_list)
        for input in inputs:
            if "building" in self.env.context:
                input.inspected_building_id = self.env.context.get(
                    "building").id
        return inputs
