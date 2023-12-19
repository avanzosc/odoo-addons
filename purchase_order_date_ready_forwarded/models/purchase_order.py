# Copyright 2020 Adrian Revilla - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class purchaseOrder(models.Model):
    _inherit = 'purchase.order'

    date_ready = fields.Date(string="Date ready", index=True)
    date_forwarded = fields.Date(string="Date forwarded", index=True)
    date_delivery = fields.Date(string='Delivery Date', copy=False)
    date_arrival = fields.Date(string='Arrival Date', copy=False)
