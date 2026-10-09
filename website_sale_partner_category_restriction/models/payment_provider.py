# Copyright 2026 AvanzOSC - Lucía Echeverría
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, fields, models

from odoo.addons.payment import utils as payment_utils


class PaymentProvider(models.Model):
    _inherit = "payment.provider"

    partner_category_ids = fields.Many2many(
        comodel_name="res.partner.category",
        relation="payment_provider_res_partner_category_rel",
        column1="provider_id",
        column2="category_id",
        string="Customer Tags",
        help="If set, only customers with at least one of these tags (on "
        "themselves or on their company) can use this payment provider.",
    )

    @api.model
    def _get_compatible_providers(
        self, company_id, partner_id, amount, *args, report=None, **kwargs
    ):
        providers = super()._get_compatible_providers(
            company_id, partner_id, amount, *args, report=report, **kwargs
        )
        categories = (
            self.env["res.partner"]
            .browse(partner_id)
            .exists()
            ._get_restriction_categories()
        )
        unavailable = providers.filtered(
            lambda p: p.partner_category_ids and not p.partner_category_ids & categories
        )
        if unavailable:
            providers -= unavailable
            payment_utils.add_to_report(
                report,
                unavailable,
                available=False,
                reason=_("not available for the customer tags"),
            )
        return providers
