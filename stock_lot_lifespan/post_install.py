# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID, fields
from dateutil.relativedelta import relativedelta


def load_alert_dates(cr, pool):
    splo = pool['stock.production.lot']
    lot_ids = splo.search(cr, SUPERUSER_ID, [('mrp_date', '!=', False),
                                             ('life_date', '!=', False)])
    for lot in splo.browse(cr, SUPERUSER_ID, lot_ids):
        mrp_date = fields.Date.from_string(lot.mrp_date)
        life_date = fields.Date.from_string(lot.life_date)
        lifespan = (life_date - mrp_date).days
        variation1 = lifespan * 0.5
        variation2 = lifespan * 0.75
        variation3 = lifespan * 0.9
        alert_vals = {
            'alert_date': mrp_date + relativedelta(days=variation1),
            'removal_date': mrp_date + relativedelta(days=variation2),
            'use_date': mrp_date + relativedelta(days=variation3)
            }
        splo.write(cr, SUPERUSER_ID, [lot.id], alert_vals)
    return
