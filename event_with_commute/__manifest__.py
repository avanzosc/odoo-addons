# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Event With Commute",
    'version': '14.0.1.0.0',
    'author': 'AvanzOSC',
    'website': 'http://www.avanzosc.es',
    'category': 'Marketing/Events',
    'license': 'AGPL-3',
    'depends': [
        'event_track_analytic',
        'sale_project',
        'product'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/event_view.xml'
    ],
    'installable': True,
}
