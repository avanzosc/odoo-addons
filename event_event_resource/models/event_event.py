# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class EventEvent(models.Model):
    _inherit = "event.event"

    resource_id = fields.Many2one(
        string="Resource", comodel_name="resource.resource")

    @api.onchange('resource_id')
    def onchange_resource_id(self):
        for event in self.filtered(lambda x: x.resource_id):
            if event.resource_id.email:
                event.teacher_zoom_email = event.resource_id.email
            if event.resource_id.password:
                event.teacher_zoom_pwd = event.resource_id.password
