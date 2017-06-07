# -*- coding: utf-8 -*-
# © 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models


class QcTriggerProductLine(models.Model):
    _inherit = "qc.trigger.product_line"

    def get_test_parents_recursively(self, test, tests=False):
        if not tests:
            tests = self.env['qc.test']
        if not test.parent_id:
            return tests
        tests |= test.parent_id
        return self.get_test_parents_recursively(test.parent_id, tests)

    def get_parent_tests(self, child_triggers):
        tests = self.env['qc.test']
        for test in child_triggers.mapped('test'):
            parents = self.get_test_parents_recursively(test, tests)
            if parents:
                tests |= parents
        return tests

    def clean_trigger_lines(self, trigger_lines):
        cleaned_trigger_lines = []
        tr_lines_recordset = self.env['qc.trigger.product_line']
        for tl in trigger_lines:
            tr_lines_recordset |= tl
        parents_lst = self.get_parent_tests(tr_lines_recordset)
        for line in trigger_lines:
            if ((line.test not in parents_lst) and not
                tr_lines_recordset.filtered(
                    lambda x: x.test.parent_id == line.test.parent_id and
                    x.partners and x.id != line.id)):
                cleaned_trigger_lines.append(line)
        return cleaned_trigger_lines

    def get_trigger_line_for_product(self, trigger, product, partner=False):
        trigger_lines = super(
            QcTriggerProductLine,
            self).get_trigger_line_for_product(trigger, product,
                                               partner=partner)
        return self.clean_trigger_lines(trigger_lines)
