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
    claim_obj = registry['crm.claim']
    timesheet_obj = registry['hr.analytic.timesheet']
    claim_ids = claim_obj.search(
        cr, SUPERUSER_ID, [('analytic_id', '!=', False)])
    for claim_id in claim_obj.browse(cr, SUPERUSER_ID, claim_ids):
        timesheet_ids = timesheet_obj.search(
            cr, SUPERUSER_ID, [('account_id', '=', claim_id.analytic_id.id)])
        for timesheet in timesheet_obj.browse(cr, SUPERUSER_ID, timesheet_ids):
            try:
                timesheet_obj.write(cr, SUPERUSER_ID, timesheet.id,
                                    {'claim_id': claim_id.id})
            except:
                continue
