# -*- coding: utf-8 -*-
# Copyright 2018 alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from openerp import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sale_gdpr = fields.Text(string='Sales', translate=True)
    purchase_gdpr = fields.Text(string='Purchases', translate=True)
    out_picking_gdpr = fields.Text(string='Out pickings', translate=True)
    in_picking_gdpr = fields.Text(string='In pickings', translate=True)
    out_invoice_gdpr = fields.Text(string='Out invoices', translate=True)
    in_invoice_gdpr = fields.Text(string='In invoices', translate=True)
