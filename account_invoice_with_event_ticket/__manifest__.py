# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    'name': "Account Invoice With Event Ticket",
    'version': '14.0.1.0.0',
    'author': 'AvanzOSC',
    'website': 'http://www.avanzosc.es',
    'category': 'Invoices & Payments',
    'license': 'AGPL-3',
    'depends': [
        'account_invoice_line_report',
        'contract',
        'sale_order_line_contract',
        'event_sale'
    ],
    'data': [
        'views/account_move_view.xml',
        'report/account_invoice_report_view.xml'
    ],
    'installable': True,
}
