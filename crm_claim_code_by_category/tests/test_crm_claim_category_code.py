# -*- coding: utf-8 -*-
# © 2016 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp.addons.crm_claim_code.tests.\
    test_crm_claim_code import TestCrmClaimCode


class TestCrmClaimCategoryCode(TestCrmClaimCode):

    def setUp(self):
        super(TestCrmClaimCategoryCode, self).setUp()
        sequence_model = self.env['ir.sequence']
        self.categ_sequence = sequence_model.create({
            'name': 'Claim Category Code',
            'padding': 4,
            'prefix': 'OTC',
        })
        categ_model = self.env['crm.case.categ']
        self.new_categ = categ_model.create({
            'name': 'Category with other sequence',
            'sequence_id': self.categ_sequence.id,
        })

    def test_new_claim_code_assign(self):
        crm_code = self._get_next_code(self.crm_sequence)
        code = self._get_next_code(self.categ_sequence)
        crm_claim = self.crm_claim_model.create({
            'name': 'Testing claim code',
            'categ_id': self.new_categ.id,
        })
        self.assertNotEqual(crm_claim.code, '/')
        self.assertNotEqual(crm_claim.code, crm_code)
        self.assertEqual(crm_claim.code, code)

    def test_copy_claim_code_assign(self):
        crm_code = self._get_next_code(self.crm_sequence)
        code = self._get_next_code(self.categ_sequence)
        self.crm_claim.write({'categ_id': self.new_categ.id})
        self.assertEqual(self.crm_claim.categ_id, self.new_categ)
        crm_claim_copy = self.crm_claim.copy()
        self.assertNotEqual(crm_claim_copy.code, self.crm_claim.code)
        self.assertNotEqual(crm_claim_copy.code, crm_code)
        self.assertEqual(crm_claim_copy.code, code)

    def _get_next_code(self, sequence):
        d = self.ir_sequence_model._interpolation_dict()
        prefix = self.ir_sequence_model._interpolate(sequence.prefix, d)
        suffix = self.ir_sequence_model._interpolate(sequence.suffix, d)
        code = (prefix + ('%%0%sd' % sequence.padding %
                          sequence.number_next_actual) + suffix)
        return code
