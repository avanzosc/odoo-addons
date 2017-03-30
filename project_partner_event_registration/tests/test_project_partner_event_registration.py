# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
import openerp.tests.common as common


class TestProjectPartnerEventRegistration(common.TransactionCase):

    def setUp(self):
        super(TestProjectPartnerEventRegistration, self).setUp()
        self.registry_obj = self.env['event.registration']
        self.project = self.browse_ref('project.project_project_3')
        self.project.calculation_type = 'date_begin'
        self.event = self.browse_ref('event.event_0')
        self.event.project_id = self.project.id

    def test_project_partner_event_registration(self):
        self.event.assign_partners()
        cond = [('event_id', '=', self.event.id),
                ('partner_id', '=', self.ref('base.user_root'))]
        registration = self.registry_obj.search(cond, limit=1)
        self.assertNotEqual(registration, False,
                            'Registration 1, not found')
        cond = [('event_id', '=', self.event.id),
                ('partner_id', '=', self.ref('base.user_demo'))]
        registration = self.registry_obj.search(cond, limit=1)
        self.assertNotEqual(registration, False,
                            'Registration 2, not found')
