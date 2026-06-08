# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    customer_id = fields.Many2one(string="Customer", comodel_name="res.partner")
    principal_activity_id = fields.Many2one(
        string="Principal Activity",
        comodel_name="principal.activity",
        related="customer_id.principal_activity_id",
        store=True,
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
        string="Water Subactivity",
        comodel_name="water.subactivity",
        related="customer_id.water_subactivity_id",
        store=True,
    )
    general_industry_subactivity_id = fields.Many2one(
        string="General Industry Subactivity",
        comodel_name="industry.subactivity",
        related="customer_id.general_industry_subactivity_id",
        store=True,
    )

    def _get_public_fields(self):
        result = super()._get_public_fields()
        result = result | {
            "customer_id",
            "principal_activity_id",
            "water_subactivity_id",
            "general_industry_subactivity_id",
        }
        return result
