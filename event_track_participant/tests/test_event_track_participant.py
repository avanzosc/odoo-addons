# Copyright (c) 2021 Berezi Amubieta - Avanzosc S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests import common
from odoo import fields


class TestEventTrackParticipant(common.SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestEventTrackParticipant, cls).setUpClass()
        cls.event_obj = cls.env['event.event']
        cls.track_obj = cls.env['event.track']
        cls.today = fields.Date.today()
        cls.event_vals = {
            'name': 'Evento',
            'date_begin': fields.Datetime.from_string('2021-11-01 08:00:00'),
            'date_end': fields.Datetime.from_string('2021-11-30 08:00:00')
            }
        cls.event = cls.event_obj.create(cls.event_vals)
        cls.track1_vals = {
            'name': 'Track1',
            'duration': 2.0,
            'event_id': cls.event.id
            }
        cls.track2_vals = {
            'name': 'Track2',
            'duration': 2.0,
            'event_id': cls.event.id
            }
        cls.track1 = cls.track_obj.create(cls.track1_vals)
        cls.track2 = cls.track_obj.create(cls.track2_vals)

    def test_product_vat_price(self):
        self.assertEqual(self.event.track_total_duration, 4.0)
