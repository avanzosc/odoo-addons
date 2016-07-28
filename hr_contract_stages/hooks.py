# -*- coding: utf-8 -*-
# © 2016 Esther Martín - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID


def assign_contract_stage(cr, registry):
    hr_obj = registry['hr.contract']
    hr_ids = hr_obj.search(cr, SUPERUSER_ID, [])
    stage_obj = registry['hr.contract.stage']
    stage_ids = stage_obj.search(cr, SUPERUSER_ID, [])
    for hr in hr_obj.browse(cr, SUPERUSER_ID, hr_ids):
        if not hr.contract_stage_id:
            try:
                vals = {'contract_stage_id': stage_ids[0]}
                hr_obj.write(cr, SUPERUSER_ID, hr.id, vals)
            except:
                continue
