# -*- coding: utf-8 -*-
# Copyright © 2017 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import openerp.tests.common as common
from openerp import exceptions


class TestPartnerParentChange(common.TransactionCase):

    def setUp(self):
        super(TestPartnerParentChange, self).setUp()
        partner_model = self.env['res.partner']
        self.wizard_model = self.env['res.partner.parent.change']
        self.parent1 = partner_model.create({
            'name': 'Parent 1',
            'is_company': True,
        })
        self.parent2 = partner_model.create({
            'name': 'Parent 2',
            'is_company': True,
        })
        self.partner = partner_model.create({
            'name': 'Partner',
            'parent_id': self.parent1.id,
        })

    def test_change_parent_no_wizard(self):
        with self.assertRaises(exceptions.Warning):
            self.partner.parent_id = self.parent2

    def test_change_parent_wizard(self):
        wizard = self.wizard_model.with_context(
            active_id=self.partner.id, active_model=self.partner._model._name
        ).create({})
        self.assertEquals(wizard.partner_id, self.partner)
        self.assertEquals(wizard.old_parent_id, self.partner.parent_id)
        self.assertEquals(wizard.old_parent_id, self.parent1)
        wizard.write({
            'new_parent_id': self.parent2.id,
        })
        self.assertEquals(self.parent1, self.partner.parent_id)
        wizard.change_parent_id()
        self.assertEquals(self.parent2, self.partner.parent_id)
