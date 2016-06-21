# -*- coding: utf-8 -*-
# (c) 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

{
    "name": "Sale Crm Lead Link",
    "version": "8.0.1.0.0",
    "license": "AGPL-3",
    "author": "AvanzOSC,",
    "website": "http://www.avanzosc.es",
    "contributors": [
        "Ainara Galdona <ainaragaldona@avanzosc.es>",
        ],
    "category": "CRM",
    "depends": ["sale_crm", ],
    "data": ["views/crm_lead_view.xml"],
    "installable": True,
    "post_init_hook": "fill_lead_in_sales",
}
