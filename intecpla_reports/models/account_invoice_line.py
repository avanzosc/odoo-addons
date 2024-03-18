# Copyright 2020 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    @api.multi
    def _compute_lots_description(self):
        for line in self:
            name = ''
            for lot in line.lot_ids:
                if not name:
                    name = lot.name
                else:
                    name = '{}, {}'.format(name, lot.name)
            line.lots_description = name

    lots_description = fields.Char(
        string='Lots descriptions', compute='_compute_lots_description')
