# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
# Copyright (c) 2019 Daniel Campos <danielcampos@avanzosc.es> - Avanzosc S.L.

from odoo import api, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.multi
    def button_approve(self, force=False):
        res = super(PurchaseOrder, self).button_approve(force)
        for line in self.order_line:
            seller = line.product_id._select_seller(
                partner_id=self.partner_id,
                quantity=line.product_qty,
                date=line.date_planned,
                uom_id=line.product_uom)
            if seller.price != line.price_unit:
                seller.price = line.price_unit
        return res
