# Copyright 2022 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Website Sale Multiple Coupon",
    "license": "AGPL-3",
    "author": "AvanzOSC",
    "website": "http://www.avanzosc.es",
    'category': 'website',
    'version': '14.0.1.0.0',
    'depends': [
        "coupon",
        "sale",
        "sale_coupon"
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml'
    ]
}
