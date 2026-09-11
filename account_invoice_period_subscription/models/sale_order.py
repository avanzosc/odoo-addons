# Copyright 2026 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _create_invoices(
        self, grouped=False, final=False, date=None, start_date=None, end_date=None
    ):
        invoices = super()._create_invoices(grouped=grouped, final=final, date=date)
        invoices.put_subscription_dates()
        return invoices
