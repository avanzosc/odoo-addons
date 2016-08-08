# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.tests.common import TransactionCase


class TestProjectClaims(TransactionCase):

    def setUp(self):
        super(TestProjectClaims, self).setUp()
        self.claim_model = self.env['crm.claim']
        self.project = self.env['project.project'].create({
            'name': 'Test Project',
        })
        self.task = self.env['project.task'].create({
            'name': 'Test Task',
            'project_id': self.project.id,
        })
        self.task2 = self.env['project.task'].create({
            'name': 'Test Task 2',
        })
        self.claim = self.claim_model.create({
            'name': 'Test Claim',
        })

    def test_claim_onchange_project(self):
        claim = self.claim_model.new()
        claim.project_id = self.project
        claim.task_id = self.task2
        self.assertEquals(claim.task_id, self.task2)
        claim.onchange_project_id()
        self.assertFalse(claim.task_id)
        self.assertEquals(claim.project_id, self.project)

    def test_claim_onchange_task(self):
        claim = self.claim_model.new()
        claim.task_id = self.task
        claim.onchange_task_id()
        self.assertEqual(claim.project_id, self.project)
        self.assertEquals(claim.task_id, self.task)

    def test_claim_write_project(self):
        self.claim.write({
            'project_id': self.project.id,
        })
        self.assertEquals(self.claim.ref, self.project)

    def test_claim_write_task(self):
        self.claim.write({
            'project_id': self.task.project_id.id,
            'task_id': self.task.id,
        })
        self.assertEquals(self.claim.ref, self.task)

    def test_claim_write_ref_project(self):
        self.claim.ref = self.project
        self.assertEquals(self.claim.project_id, self.project)
        self.assertEquals(self.project.claim_count,
                          len(self.project.claim_ids))
        self.assertEquals(self.project.claim_count, 1)

    def test_claim_write_ref_task(self):
        self.claim.ref = self.task
        self.assertEquals(self.claim.task_id, self.task)
        self.assertEquals(self.task.claim_count,
                          len(self.task.claim_ids))
        self.assertEquals(self.task.claim_count, 1)
        self.assertEquals(self.claim.project_id, self.task.project_id)
        self.assertEquals(self.claim.project_id, self.project)
        self.assertEquals(self.project.claim_count,
                          len(self.project.claim_ids))
        self.assertEquals(self.project.claim_count, 1)
