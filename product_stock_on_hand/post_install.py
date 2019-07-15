# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID


def update_stock_on_hand_locations(cr, pool):
    slo = pool['stock.location']
    location_ids = slo.search(cr, SUPERUSER_ID, [('usage', '=', 'internal')])
    if location_ids:
        slo.write(cr, SUPERUSER_ID, location_ids, {'stock_on_hand': True})
    return
