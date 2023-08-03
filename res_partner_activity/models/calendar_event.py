# Copyright 2023 Berezi Amubieta - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    partner_customer_id = fields.Many2one(
        string="Customer",
        comodel_name="res.partner")
    principal_activity_id = fields.Many2one(
        string="Principal Activity",
        comodel_name="principal.activity",
        related="partner_customer_id.principal_activity_id",
        store=True)
    water_subactivity_id = fields.Many2one(
        string="Water Subactivity",
        comodel_name="water.subactivity",
        related="partner_customer_id.water_subactivity_id",
        store=True)
    general_industry_subactivity_id = fields.Many2one(
        string="General Industry Subactivity",
        comodel_name="industry.subactivity",
        related="partner_customer_id.general_industry_subactivity_id",
        store=True)

    def _get_public_fields(self):
        result = super(CalendarEvent, self)._get_public_fields()
        result = result | {
            'partner_customer_id', 'principal_activity_id',
            'water_subactivity_id', 'general_industry_subactivity_id'}
        return result
