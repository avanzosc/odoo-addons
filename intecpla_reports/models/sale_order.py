# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _compute_print_commitment_date(self):
        for sale in self:
            print_commitment_date = False
            lines = sale.order_line.filtered(lambda x: x.commitment_date)
            if lines:
                print_commitment_date = True
            sale.print_commitment_date = print_commitment_date

    print_commitment_date = fields.Boolean(
        string='Print commitment date',
        compute='_compute_print_commitment_date')
