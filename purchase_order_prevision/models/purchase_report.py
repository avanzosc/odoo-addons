# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    estimated_payment_date = fields.Date(string="Estimated payment date", readonly=True)

    def _select(self):
        return "%(select)s, %(new_field)s" % {
            "select": super()._select(),
            "new_field": "po.estimated_payment_date as estimated_payment_date",
        }

    def _group_by(self):
        return "%(group_by_str)s, %(new_field)s" % {
            "group_by_str": super()._group_by(),
            "new_field": "po.estimated_payment_date",
        }
