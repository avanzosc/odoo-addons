# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import tools
from PIL import Image
import StringIO


class TestMailDocument(common.TransactionCase):

    def setUp(self):
        super(TestMailDocument, self).setUp()
        image = Image.new('RGB', (1920, 1080))
        output = StringIO.StringIO()
        image.save(output, "PNG")
        self.contents = output.getvalue().encode("base64")
        output.close()

    def test_chatter_send_attachment(self):
        body_text = 'Body Text'
        partner = self.env['res.partner'].create({'name': 'Test partner'})
        attachment = self.env['ir.attachment'].create({
            'name': partner.name,
            'datas_fname': 'image.png',
            'datas': self.contents,
        })
        kwargs = {'attachment_ids': attachment.ids}
        partner.message_post(
            body=body_text, type='comment', content_subtype='plaintext',
            **kwargs)
        self.assertEquals(
            tools.html2plaintext(attachment.description),
            u'{}\n'.format(body_text))
