# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMoveLline(models.Model):
    _inherit = 'account.move.line'

    def _compute_student_name(self):
        for line in self:
            if not line.move_id.print_students:
                line.student_name = ""
            else:
                super(AccountMoveLline, line)._compute_student_name()
