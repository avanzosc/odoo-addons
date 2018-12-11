# Copyright 2018 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo.tests import common


class TestPartnerSuccessStory(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestPartnerSuccessStory, cls).setUpClass()
        cls.partner = cls.env['res.partner'].create({
            'name': 'New Partner',
        })
        cls.success_story = cls.env['res.partner.success_story'].create({
            'partner_id': cls.partner.id,
            'name': 'Success Story for New Partner',
        })

    def test_partner_success_story(self):
        self.assertEquals(self.partner.success_story_count, 1)
        action_dict = self.partner.button_open_success_stories()
        self.assertEqual(
            action_dict.get('res_model'), 'res.partner.success_story')
