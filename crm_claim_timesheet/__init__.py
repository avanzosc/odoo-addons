# -*- coding: utf-8 -*-
# (Copyright) 2017 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from . import models
from openerp import SUPERUSER_ID


def assign_claims_to_project(cr, registry):
    """
    This post-init-hook will update all existing project assigning them the
    corresponding claims.
    """
    cond = []
    claim_obj = registry['crm.claim']
    timesheet_obj = registry['hr.analytic.timesheet']
    claim_ids = claim_obj.search(
        cr, SUPERUSER_ID, [('analytic_id', '!=', False)])
    for claim_id in claim_obj.browse(cr, SUPERUSER_ID, claim_ids):
        cond1 = ('account_id', '=', claim_id.analytic_id.id)
        cond.append(cond1)
        if claim_id.task_id:
            cond.append(('task_id', '=', claim_id.task_id))
        try:
            timesheet_ids = timesheet_obj.search(cr, SUPERUSER_ID, cond)
        except:
            timesheet_ids = timesheet_obj.search(cr, SUPERUSER_ID, cond1)
        for timesheet in timesheet_ids:
            try:
                timesheet_obj.write(cr, SUPERUSER_ID, timesheet,
                                    {'claim_id': claim_id.id})
            except:
                continue
