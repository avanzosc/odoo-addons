# -*- coding: utf-8 -*-
# Copyright 2017 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from . import models

from openerp import SUPERUSER_ID


def update_sale_order_origin_name(cr, pool):
    cr.execute("UPDATE sale_order SET origin_name = sale_order.name;")
    return
