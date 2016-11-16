# -*- coding: utf-8 -*-
# © 2016 Ainara Galdona - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields


class PaymentMode(models.Model):

    _inherit = "payment.mode"

    transfer_payment_mode = fields.Many2one(
        comodel_name='payment.mode', string='Transfer Payment Mode')
