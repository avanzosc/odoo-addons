# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import fields
import openerp.tests.common as common


class TestCrmProject(common.TransactionCase):

    def setUp(self):
        super(TestCrmProject, self).setUp()
        self.partner_id = self.env['res.partner'].create({
            'name': 'Partner for test',
        })
        self.project_id = self.env['project.project'].create({
            'name': 'Project for test',
            'partner_id': self.partner_id.id,
        })
        self.call_id = self.env['crm.phonecall'].create({
            'name': 'Call for test',
            'partner_id': self.partner_id.id,
            'project_id': self.project_id.id,
        })
        self.meeting_id = self.env['calendar.event'].create({
            'name': 'Meeting for test',
            'start': fields.Datetime.now(),
            'stop': fields.Datetime.now(),
            'project_id': self.project_id.id,
        })

    def test_project_partner(self):
        self.assertTrue(self.partner_id.project_ids)
        self.assertEquals(self.partner_id.project_count, 1)

    def test_project_phonecall(self):
        self.assertTrue(self.project_id.phonecall_ids)
        self.assertEquals(self.project_id.phonecall_count, 1)

    def test_project_meeting(self):
        self.assertTrue(self.project_id.meeting_ids)
        self.assertEquals(self.project_id.meeting_count, 1)
