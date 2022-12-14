# Copyright 2022 Alfredo de la Fuente - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _prepare_picking(self):
        vals = super(PurchaseOrder, self)._prepare_picking()
        if self.order_type:
            vals['purchase_type_id'] = self.order_type.id
        return vals

    def _prepare_invoice(self):
        vals = super(PurchaseOrder, self)._prepare_invoice()
        if self.order_type:
            vals['purchase_type_id'] = self.order_type.id
        return vals
