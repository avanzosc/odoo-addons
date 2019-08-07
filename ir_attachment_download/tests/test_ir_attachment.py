# Copyright 2019 Mikel Arregi Etxaniz - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import odoo.tests.common as common
import base64


@common.at_install(False)
@common.post_install(True)
class IrAttachment(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(IrAttachment, cls).setUpClass()
        cls.wiz_obj = cls.env['attach.download.action']
        cls.attachment = cls.env['ir.attachment'].create({
            'name': 'Attach1',
            'datas': base64.b64encode(b"avanzosc")
        })
        cls.property_field = cls.env['ir.model.fields'].search([
            ('ttype', '=', 'binary')], limit=1)
        cls.property = cls.env['ir.property'].create({
            'name': 'Property to test',
            'value_binary': cls.attachment.datas,
            'fields_id': cls.property_field.id,
        })

    def test_attachment_downloader(self):
        wiz = self.wiz_obj.create({
            'name': 'Download',
            'model_id': self.env['ir.model'].search([
                ('model', '=', 'ir.property')], limit=1).id,
        })
        wiz.create_action_server()
        action = self.env['ir.actions.server'].search(
            [('name', '=', 'Download')])
        self.assertTrue(action)
