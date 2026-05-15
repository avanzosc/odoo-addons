# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    principal_activity_id = fields.Many2one(
        string="Principal Activity", comodel_name="principal.activity"
    )
    principal_activity_water = fields.Boolean(
        string="Water Principal Activity",
        related="principal_activity_id.water",
        store=True,
    )
    principal_activity_industry = fields.Boolean(
        string="Industry Principal Activity",
        related="principal_activity_id.industry",
        store=True,
    )
    water_subactivity_id = fields.Many2one(
        string="Water Subactivity", comodel_name="water.subactivity"
    )
    general_industry_subactivity_id = fields.Many2one(
        string="General Industry Subactivity", comodel_name="industry.subactivity"
    )

    flowserve_manager_id = fields.Many2one(
        comodel_name="responsable.flowserv",
        string="*Flowserve Manager",
        index=True,
        ondelete="restrict",
    )
    schedule = fields.Char()
    what_do_they_do = fields.Char()
    managing_entity_id = fields.Many2one(
        comodel_name="res.partner",
        string="Managing Entity",
        index=True,
    )
    interest_id = fields.Many2one(
        comodel_name="res.partner.interes",
        string="Interest",
        index=True,
        ondelete="restrict",
    )

    @api.onchange("principal_activity_id")
    def _onchange_principal_activity(self):
        if self.principal_activity_id:
            if not self.principal_activity_water:
                self.water_subactivity_id = False
            if not self.principal_activity_industry:
                self.general_industry_subactivity_id = False
