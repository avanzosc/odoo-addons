# Copyright 2021 Alfredo de la fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import fields, models


class ProductPricelist(models.Model):
    _name = "product.pricelist"
    _inherit = [
        "product.pricelist",
        "portal.mixin",
        "mail.thread",
        "mail.activity.mixin",
    ]

    currency_id = fields.Many2one(tracking=True)
    discount_policy = fields.Selection(tracking=True)
