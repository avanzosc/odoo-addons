# Copyright 2020 Oihane Crucelaegui - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailMassMailingContact(models.Model):
    _inherit = "mail.mass_mailing.contact"

    @api.multi
    def find_or_create(self, partner, mail_list):
        contacts = self.search([
            ("partner_id", "=", partner.id),
        ])
        contact = (contacts.filtered(
            lambda c: mail_list in c.list_ids) or contacts[:1])
        if not contact:
            contact = self.create({
                "partner_id": partner.id,
                "company_name": partner.company_id.name,
                "name": partner.name,
            })
        return contact
