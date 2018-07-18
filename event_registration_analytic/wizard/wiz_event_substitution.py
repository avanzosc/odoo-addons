# -*- coding: utf-8 -*-
# (c) 2017 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import models


class WizEventSubstitution(models.TransientModel):
    _inherit = 'wiz.event.substitution'

    def substitution_employee_from_thread(self):
        res = super(
            WizEventSubstitution, self).substitution_employee_from_thread()
        for line in self.lines:
            line.event._compute_seats()
        return res
