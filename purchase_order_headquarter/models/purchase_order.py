# Copyright 2021 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    headquarter_id = fields.Many2one(
        string='Headquarter', comodel_name='res.partner',
        domain="[('headquarter','=', True)]")
