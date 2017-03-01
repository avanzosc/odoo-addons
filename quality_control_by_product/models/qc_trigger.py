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

    def get_trigger_line_for_product(self, trigger, product, partner=False):
        trigger_lines = super(
            QcTriggerProductLine,
            self).get_trigger_line_for_product(trigger, product,
                                               partner=partner)
        lines = self.env['qc.trigger.product_line']
        for line in trigger_lines:
            lines |= line
        parent_tests = self.get_parent_tests(
            lines.filtered(lambda x: x.test.parent_id))
        return set(lines.filtered(lambda x: x.test not in parent_tests))
