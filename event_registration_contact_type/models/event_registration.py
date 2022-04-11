# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    contact_type_id = fields.Many2one(
        string='Contact type', comodel_name='res.partner.type', store=True,
        compute='_compute_contact_type_id')

    @api.depends("partner_id", "partner_id.contact_type_id",
                 "customer_id", "customer_id.contact_type_id")
    def _compute_contact_type_id(self):
        for registration in self:
            contact_type = False
            if (registration.partner_id and
                    registration.partner_id.contact_type_id):
                contact_type = registration.partner_id.contact_type_id
            if (registration.customer_id and
                    registration.customer_id.contact_type_id):
                contact_type = registration.customer_id.contact_type_id
            registration.write({'contact_type_id': contact_type.id if contact_type else False})
