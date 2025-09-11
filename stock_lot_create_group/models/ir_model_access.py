# Copyright 2024 Berezi Amubieta - AvanzOSC
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class IrModelAccess(models.Model):
    _inherit = "ir.model.access"

    @api.model
    def init(self):
        try:
            group_inventory_stock_lot = self.env.ref(
                "stock.access_stock_production_lot_user"
            )
            if group_inventory_stock_lot:
                group_inventory_stock_lot.write(
                    {"perm_create": False, "perm_unlink": False}
                )
        except Exception:
            pass
