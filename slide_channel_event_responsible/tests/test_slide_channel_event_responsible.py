# Copyright 2021 Alfredo de la Fuente - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo.tests import common
from odoo.tests import tagged


@tagged("post_install", "-at_install")
class TestSlideChannelEventResponsible(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSlideChannelEventResponsible, cls).setUpClass()
        cls.user_obj = cls.env['res.users']
        cls.event_obj = cls.env['event.event']
        cls.slide_channel_partner_obj = cls.env['slide.channel.partner']
        cls.slide_channel_obj = cls.env['slide.channel']
        cls.event_stage_new = cls.env.ref("event.event_stage_new")
        cls.event_stage_confirm = cls.env.ref("event.event_stage_announced")
        vals = {'name': 'User 1 for slide channel event_responsible',
                'login': 'login1@avanzosc.es'}
        cls.user1 = cls.user_obj.create(vals)
        vals = {'name': 'User 2 for slide channel event_responsible',
                'login': 'login2@avanzosc.es'}
        cls.user2 = cls.user_obj.create(vals)
        vals = {'name': 'User 3 for slide channel event_responsible',
                'login': 'login3@avanzosc.es'}
        cls.user3 = cls.user_obj.create(vals)
        cond = [('stage_id', '=', cls.event_stage_new.id)]
        cls.event = cls.event_obj.search(cond, limit=1)
        cls.event.write({
            'user_id': cls.user1.id,
            'main_responsible_id': cls.user2.id,
            'second_responsible_id': cls.user3.id})
        cls.slide_channel = cls.slide_channel_obj.search([], limit=1)
        cls.slide_channel.event_ids = [(6, 0, cls.event.ids)]

    def test_slide_channel_event_responsible(self):
        self.event.stage_id = self.event_stage_confirm.id
        cond = [('channel_id', '=', self.slide_channel.id),
                ('partner_id', 'in', (self.user1.partner_id.id,
                                      self.user2.partner_id.id,
                                      self.user3.partner_id.id))]
        slide_channel_partners = self.slide_channel_partner_obj.search(cond)
        self.assertEqual(len(slide_channel_partners), 3)
