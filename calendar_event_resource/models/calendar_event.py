# Copyright 2022 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    resource_id = fields.Many2one(
        string="Resource", comodel_name="resource.resource")

    @api.model
    def _get_public_fields(self):
        result = super(CalendarEvent, self)._get_public_fields()
        result = result | {'resource_id'}
        return result
