# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    price_subtotal_eur = fields.Float('Total EUR', readonly=True)
    origin_price_subtotal = fields.Float('Origin total', readonly=True)

    def _select(self):
        select = super(PurchaseReport, self)._select()
        new_select = "{}, {}".format(
            select, "sum(l.price_subtotal_eur) as price_subtotal_eur")
        new_select = "{}, {}".format(
            new_select,
            "sum(l.origin_price_subtotal) as origin_price_subtotal")
        return new_select
