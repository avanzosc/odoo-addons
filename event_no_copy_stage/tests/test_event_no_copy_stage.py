# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo.tests import common


class TestEventNoCopyStage(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestEventNoCopyStage, cls).setUpClass()
        cls.new_stage = cls.env.ref('event.event_stage_new')
        cls.done_stage = cls.env.ref('event.event_stage_done')
        cond = [('stage_id', '=', cls.done_stage.id)]
        cls.event = cls.env['event.event'].search(cond, limit=1)

    def test_event_no_copy_stage(self):
        new_event = self.event.copy()
        self.assertEqual(new_event.stage_id.id, self.new_stage.id)
