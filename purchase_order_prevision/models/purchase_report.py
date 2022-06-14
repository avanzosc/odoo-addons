# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    estimated_payment_date = fields.Date(
        string="Estimated payment date", readonly=True)

    def _select(self):
        select = super(PurchaseReport, self)._select()
        new_select = "{}, {}".format(
            select, "s.estimated_payment_date as estimated_payment_date")
        return new_select

    def _group_by(self):
        group_by_str = super(PurchaseReport, self)._group_by()
        new_group_by_str = "{}, {}".format(
            group_by_str, "s.estimated_payment_date")
        return new_group_by_str
