# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from . import models
from openerp import SUPERUSER_ID


def fill_lead_in_sales(cr, registry):
    lead_obj = registry['crm.lead']
    sale_obj = registry['sale.order']
    lead_ids = lead_obj.search(cr, SUPERUSER_ID, [('ref', '!=', False)])
    for lead in lead_obj.browse(cr, SUPERUSER_ID, lead_ids):
        if lead.ref._name == 'sale.order':
            try:
                sale_obj.write(cr, SUPERUSER_ID, lead.ref.id,
                               {'lead_id': lead.id})
            except:
                continue
