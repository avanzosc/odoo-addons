# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models

import logging

_logger = logging.getLogger(__name__)

class SurveyUserInput(models.Model):
    _inherit = "survey.user_input"

    inspected_building_id = fields.Many2one(
        string="Inspected Building",
        comodel_name="res.partner",
        copy=False,
    )
    maintainer_id = fields.Many2one(
        related="inspected_building_id.maintainer_id",
        string="Maintainer",
        comodel_name="res.partner",
    )
    installer_id = fields.Many2one(
        related="inspected_building_id.installer_id",
        string="Installer",
        comodel_name="res.partner",
    )
    administrator_id = fields.Many2one(
        related="inspected_building_id.administrator_id",
        string="Administrator",
        comodel_name="res.partner",
    )

    building_section_id = fields.Many2one(
        string="Building Section/Area",
        comodel_name="building.section",
        copy=False,
    )
    section_ids = fields.One2many(
        string="Inspected Building Section/Area",
        comodel_name="building.section",
        copy=False,
        related="inspected_building_id.building_section_ids",
    )
    building_use_id = fields.Many2one(
        string="Building type",
        comodel_name="building.use",
        related="inspected_building_id.building_use_id",
        store=True,
        copy=False,
    )
    risk = fields.Char(
        string="Risk", related="building_section_id.risk", store=True, copy=False
    )
    superficie = fields.Float(
        string="Superficie",
        related="building_section_id.superficie",
        store=True,
        copy=False,
    )
    file_number = fields.Char(
        string="File Number",
        related="inspected_building_id.file_number",
        store=True,
        copy=False,
    )
    act_number = fields.Char(
        string="Act Number",
        copy=False,
    )
    inspection_start_date = fields.Datetime(
        string="Inspection Start Date",
        copy=False,
    )
    inspection_end_date = fields.Datetime(
        string="Inspection End Date",
        copy=False,
    )
    inspector_id = fields.Many2one(
        string="Inspector",
        comodel_name="res.partner",
        copy=False,
    )
    inspection_type = fields.Selection(
        selection=[("periodic", _("Periodic")), ("volunteer", _("Volunteer"))],
        string="Inspection Type",
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        inputs = super(SurveyUserInput, self).create(vals_list)
        for input in inputs:
            if "building" in self.env.context:
                input.inspected_building_id = self.env.context.get("building").id
        return inputs
    
    def action_start_survey(self):
        
        # Obtener el ID del partner con nombre "admin"
        current_user_partner = self.env.user.partner_id

        if current_user_partner:
            # Asignar el ID del socio asociado con el usuario actual al partner_id del survey_user_input
            self.partner_id = current_user_partner.id
        else:
            # Usuario administrador es id = 3
            self.partner_id = 3
            
        
        base_url = request.httprequest.base_url
        if not base_url:
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            
        survey_id = self.survey_id
        access_token = survey_id.access_token
        answer_token = self.access_token
        url = "{}/survey/start/{}?answer_token={}".format(base_url, access_token, answer_token)
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'self',
        }