# Copyright 2022 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    saca_id = fields.Many2one(
        string="Saca", comodel_name="saca", related="saca_line_id.saca_id", store=True
    )
    saca_line_id = fields.Many2one(
        string="Saca Line", comodel_name="saca.line", copy=False
    )

    def button_confirm(self):
        result = super().button_confirm()
        for picking in self.picking_ids:
            for m in picking.move_ids_without_package:
                if m.purchase_line_id:
                    m.standard_price = m.purchase_line_id.price_unit
                    m.onchange_standard_price()
                for ml in m.move_line_ids:
                    ml.standard_price = m.purchase_line_id.price_unit
                    ml.onchange_standard_price()
        return result
