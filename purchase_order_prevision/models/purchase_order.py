# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from dateutil.relativedelta import relativedelta


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    loading_date = fields.Date(
        string="Loading Date", index=True)
    estimated_payment_date = fields.Date(
        string="Estimated payment date", index=True, store=True,
        compute="_compute_estimated_payment_date")
    date_planned_without_hour = fields.Date(
        string='Expected Date', index=True, store=True,
        compute='_compute_date_planned_without_hour')

    @api.depends("date_planned", "loading_date", "payment_term_id")
    def _compute_estimated_payment_date(self):
        for purchase in self.filtered(
            lambda x: x.date_planned and x.payment_term_id and
                x.payment_term_id.line_ids):
            estimated_payment_date = False
            date = (purchase.loading_date if purchase.loading_date else
                    purchase.date_planned.date())
            line = purchase.payment_term_id.line_ids[0]
            if line.days:
                estimated_payment_date = (
                    date + relativedelta(days=line.days - 1))
            if line.weeks:
                estimated_payment_date = (
                    date + relativedelta(weeks=line.weeks))
            if line.months:
                estimated_payment_date = (
                    date + relativedelta(months=line.months))
            if estimated_payment_date:
                purchase.estimated_payment_date = estimated_payment_date

    @api.depends("date_planned")
    def _compute_date_planned_without_hour(self):
        for purchase in self.filtered(lambda x: x.date_planned):
            purchase.date_planned_without_hour = purchase.date_planned.date()
