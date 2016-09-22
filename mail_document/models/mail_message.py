# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import api, models
from openerp import tools


class MailMessage(models.Model):
    _inherit = 'mail.message'

    @api.model
    def create(self, values):
        body = tools.html2plaintext(values.get('body'))
        attachment_ids = values.get('attachment_ids')
        attach_ids = []
        for attachment_id in attachment_ids:
            if attachment_id[0] == 4:
                attach_ids = [attachment_id[1]]
            elif attachment_id[0] == 6:
                attach_ids = attachment_id[2]
        attachments = self.env['ir.attachment'].browse(attach_ids)
        attachments.write({
            'description': body,
        })
        return super(MailMessage, self).create(values)
