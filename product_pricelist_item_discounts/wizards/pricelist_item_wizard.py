# Copyright 2023 Leire Martinez de Santos - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import RedirectWarning
from odoo.models import expression
from odoo.tools.safe_eval import safe_eval


class CreateProductPricelistItemDiscounts(models.TransientModel):
    _name = "create.pricelist_item.discount"
    _description = "Wizard to apply pricelist item discounts"

    discount = fields.Float(string="Discount", required=True)
    confirm_text = fields.Char('Confirm Text')
    positive = fields.Boolean('Positive', help="Apply increment on price")

    @api.multi
    def button_apply_discounts(self):
        self.ensure_one()
        selected_ids = self.env.context.get('active_ids', [])
        item_ids = self.env['product.pricelist.item'].browse(selected_ids)
        item_ids.apply_discount(self.discount, positive=self.positive)
