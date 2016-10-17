# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class AccountInvoiceLine(models.Model):

    _inherit = 'account.invoice.line'

    lot_id = fields.Many2one(comodel_name='stock.production.lot',
                             string="Lot")
