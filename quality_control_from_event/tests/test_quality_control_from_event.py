# -*- coding: utf-8 -*-
# (c) 2016 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestQualityControlFromEvent(common.TransactionCase):

    def setUp(self):
        super(TestQualityControlFromEvent, self).setUp()
        self.event_model = self.env['event.event']
        self.inspection_model = self.env['qc.inspection']
        event_vals = {'name': 'inspection from event',
                      'date_begin': '2020-01-01 15:00:00',
                      'date_end': '2020-01-15 21:00:00'}
        self.event = self.event_model.create(event_vals)

    def test_quality_control_from_event(self):
        inspection_vals = {'object_id': ('event.event,' +
                                         str(self.event.id))}
        self.inspection = self.inspection_model.create(inspection_vals)
        self.event.inspections_from_event()
        self.assertNotEqual(
            self.event.inspections_count, 0,
            'Event without inspections')
