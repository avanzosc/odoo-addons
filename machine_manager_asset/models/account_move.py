# Copyright 2024 Alfredo de la Fuente - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_post(self):
        res = super().action_post()
        for invoice in self.filtered(lambda z: z.move_type == "in_invoice"):
            lines = invoice.invoice_line_ids.filtered(
                lambda x: x.display_type == "product"
                and x.product_id.machine_ok
                and x.asset_profile_id
                and x.asset_profile_id.asset_product_item
                and x.asset_id
                and x.purchase_line_id
            )
            if lines:
                lines._put_asset_in_machine()
        return res
