# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import SUPERUSER_ID


def load_depreciation_line_percentage(cr, pool):
    aaao = pool['account.asset.asset']
    aadlo = pool['account.asset.depreciation.line']
    asset_ids = aaao.search(cr, SUPERUSER_ID,
                            [('method_time', '=', 'percentage')])
    dep_line_ids = aadlo.search(cr, SUPERUSER_ID,
                                [('asset_id', 'in', asset_ids)])
    for dep_line in aadlo.browse(cr, SUPERUSER_ID, dep_line_ids):
        aadlo.write(cr, SUPERUSER_ID, [dep_line.id],
                    {'method_percentage': dep_line.asset_id.method_percentage})
    return
