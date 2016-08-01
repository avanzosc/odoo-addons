# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID


def assign_contract_stage(cr, registry):
    stage_obj = registry['hr.contract.stage']
    stage_ids = stage_obj.search(cr, SUPERUSER_ID, [], order="sequence")
    if stage_ids:
        cr.execute('UPDATE hr_contract '
                   'SET contract_stage_id = \'%s\' '
                   'WHERE contract_stage_id IS NULL;' %
                   (stage_ids[0]))
